# Project Research Summary

**Project:** CalendarPlanner v2.1 — Privacy, Reminders & Multi-Year Budget
**Domain:** Household calendar + budget planner (2-user, Polish locale, Google Calendar sync)
**Researched:** 2026-03-20
**Confidence:** HIGH

## Executive Summary

CalendarPlanner v2.1 is a feature-completion milestone that activates backend capabilities already built in v1.1–v2.0 but never exposed to users. Event privacy (visibility toggle, filtering) is ~90% shipped — the data model, repository filtering, sync pipeline, and even the form UI exist. Reminder configuration has a complete backend pipeline (schema, validation, Google sync) but zero UI. Multi-year budget browsing already works via year-parameterized API and navigation arrows. The research conclusion is clear: **this is primarily a frontend wiring and data-integrity milestone, not a greenfield build.** Zero new Python packages are needed. Zero database migrations are required for the core features.

The recommended approach is to validate existing implementations first (privacy), then wire missing UI to existing backends (reminders), then fix data-model gaps that make multi-year browsing inaccurate (carry-forward balance, recurring expense year-scoping), and finally build the one genuinely new feature (year-over-year comparison). The biggest risk is **data integrity in multi-year budget views**: the current single-row `BudgetSettings` and year-unscoped recurring expenses produce incorrect numbers for any year other than the current one. These must be fixed before shipping year navigation, or users will see wrong data and lose trust. The secondary risk is **Google Calendar sync consistency** — changing event visibility from shared to private must delete the event from the partner's Google Calendar, which is not currently handled.

## Key Findings

### Recommended Stack

No stack changes. The existing FastAPI 0.135.1 + Pydantic 2.10.6 + google-api-python-client 2.93.0 + Jinja2 + Supabase (httpx) + Tailwind CSS stack covers every v2.1 feature. No new pip packages, no version upgrades, no frontend libraries.

**Core technologies (all existing, all sufficient):**
- **FastAPI**: Routes, dependency injection, query params for year navigation — all patterns proven in v2.0
- **Pydantic**: `EventCreate`/`EventUpdate` already validate `visibility`, `reminder_minutes_list` with range constraints
- **google-api-python-client**: Calendar v3 API stable; reminder overrides (max 5, popup/email, 0–40320 min) already implemented in `_event_body()`
- **Vanilla JS + Jinja2 templates**: New UI (reminder chips, comparison table) follows existing patterns; no framework addition warranted

**Explicitly rejected:** Alpine.js, htmx, Chart.js, any ORM, Celery, WebSocket/SSE, any new pip package.

### Expected Features

**Must have (P1 — table stakes):**
- Visibility toggle in event form (wired to existing `shared`/`private` field)
- Private event filtering verified across ALL calendar view routes
- Reminder on/off toggle with household defaults (30 min + 2 days)
- Multi-year budget navigation (remove any frontend year restrictions)
- Budget carry-forward balance (year N ending → year N+1 starting)
- Year-over-year comparison summary (side-by-side annual totals)

**Should have (P2 — differentiators):**
- Custom reminder entries (add/remove up to 5 per event)
- Lock icon indicator for private events on calendar grid
- Color-coded YoY delta indicators (green ↑ improvement / red ↓ decline with percentages)
- Reminder method choice (popup vs email)

**Defer (v2.2+):**
- User-level default reminder preferences
- Budget data import (Excel/CSV)
- Busy/free display for private events
- Per-year budget settings UI

### Architecture Approach

The architecture is a clean layered stack: Jinja2 templates → FastAPI routes → service layer → repository layer → SupabaseStore (httpx). All v2.1 features modify existing files — **zero new files created, 5–7 existing files modified, zero database migrations.** The event privacy pipeline is fully wired end-to-end. Reminder UI needs 3 file modifications (modal HTML, calendar JS, day events partial). YoY comparison adds a service method + API endpoint + UI section to existing files.

**Major components (all existing):**
1. **Event pipeline** (models → schemas → repository → service → routes → templates) — privacy and reminders are field additions to this pipeline
2. **Budget pipeline** (overview_service → overview_routes → budget_overview template) — comparison extends this with one new method + endpoint
3. **Google Sync pipeline** (GoogleSyncService → `_event_body` → `_sync_recipients`) — must add `_retract_from_non_recipients` for visibility changes

### Critical Pitfalls

1. **Visibility change doesn't clean up partner's Google Calendar** — When event changes shared→private, it persists in partner's Google Calendar. Must add `_retract_from_non_recipients` deletion step in sync service. Ship WITH the visibility toggle, not after.

2. **Initial balance is not year-scoped** — `BudgetSettings.initial_balance` is a single value applied to ALL years. Year N+1 must compute its starting balance from year N's ending balance. Fix BEFORE enabling year navigation.

3. **Recurring expenses appear in all years** — `get_by_calendar_year` fetches recurring expenses (`month=0`) without year filtering. A 2026 recurring expense shows in 2024 view. Add `year <= requested_year` filter to recurring expense queries.

4. **Google Calendar API rejects >5 reminder overrides** — No list-length validation in schema. Events with 6+ reminders fail to sync silently. Add `max_length=5` to schema AND cap in UI.

5. **Dual reminder fields create ambiguous state** — Both `reminder_minutes` (legacy int) and `reminder_minutes_list` (new list) coexist. UI must write exclusively to `reminder_minutes_list` and null out the legacy field. Migrate existing data.

6. **Private event import doesn't enforce ownership** — Google Calendar import attributes all events to the importing user, bypassing `cp_owner_id`. Must validate ownership extended property on import to prevent partner claiming private events.

## Implications for Roadmap

Based on combined research, dependency analysis, and pitfall ordering:

### Phase 1: Event Privacy — Validate & Harden
**Rationale:** Already ~90% complete; needs verification, Google sync cleanup path, and import guard. Lowest effort, highest immediate trust impact. No dependencies on other features.
**Delivers:** Fully working private events — invisible to partner on web AND Google Calendar, safe through import/export round-trips.
**Features:** Visibility toggle verification, private event filtering across all views, lock icon indicator, sync retraction on visibility change, import ownership validation.
**Avoids:** Pitfall 1 (sync cleanup), Pitfall 2 (export_month leak), Pitfall 8 (import ownership), Pitfall 11 (form population on edit).
**Research needed:** NO — code is reviewed, patterns are clear, changes are well-scoped.

### Phase 2: Reminder UI — Wire Frontend to Existing Backend
**Rationale:** Self-contained frontend task. Backend is complete (schema, validation, Google sync). No dependency on budget features. Clearing event-related work before moving to budget.
**Delivers:** Reminder toggle with defaults, chip-based multi-reminder editor, Google Calendar sync of configured reminders.
**Features:** Reminder on/off toggle, default presets (30 min + 2 days), add/remove custom entries (up to 5), i18n labels.
**Avoids:** Pitfall 6 (max 5 overrides — enforce in schema + UI), Pitfall 7 (dual fields — write only to list, null legacy), Pitfall 9 (tri-state: none/default/custom), Pitfall 11 (populate reminders on edit).
**Research needed:** NO — Google Calendar API constraints verified via Context7, UI pattern matches existing chip/pill design.

### Phase 3: Multi-Year Budget — Fix Data Integrity & Enable Navigation
**Rationale:** Must fix carry-forward balance and recurring expense scoping BEFORE users can navigate years, otherwise they see incorrect data. This is a data-integrity prerequisite for Phase 4.
**Delivers:** Accurate budget data for any past/future year, carry-forward balance computation, year-scoped recurring expenses, polished year navigation UX.
**Features:** Budget carry-forward balance, multi-year navigation (verified), recurring expense year filtering, "Calculations use current rates" disclaimer.
**Avoids:** Pitfall 3 (initial balance not year-scoped), Pitfall 4 (recurring expenses in wrong years), Pitfall 5 (rates not year-versioned — document limitation, defer full fix).
**Research needed:** MAYBE — carry-forward computation strategy (dynamic vs snapshot) needs validation during planning. Likely straightforward for <5 years of data.

### Phase 4: Year-over-Year Comparison — New Feature Build
**Rationale:** Depends on Phase 3 (multi-year data must be accurate). The only genuinely new feature — new service method, new API endpoint, new UI section. Highest complexity.
**Delivers:** Side-by-side annual summary comparison, delta calculations, expandable comparison panel in budget overview.
**Features:** YoY comparison summary, delta indicators (color-coded), no-data vs zero distinction for empty years, i18n labels.
**Avoids:** Pitfall 10 (misleading zeros — distinguish no-data from zero-value months).
**Research needed:** NO — architecture doc provides complete service method design, API endpoint spec, and UI wireframe. Standard patterns.

### Phase Ordering Rationale

- **Privacy before reminders:** Both touch the event form, but privacy is nearly complete and validates existing code. Shipping privacy first means the form infrastructure is verified before adding reminder controls.
- **Reminders before budget:** Clears all event-pipeline work before context-switching to budget pipeline. Reduces cognitive overhead.
- **Multi-year data integrity before comparison:** Comparison is presentation of multi-year data. If the underlying data is wrong (Pitfalls 3, 4, 5), the comparison is meaningless. Fix the foundation first.
- **Features grouped by pipeline:** Phases 1–2 are event pipeline. Phases 3–4 are budget pipeline. This minimizes file-switching and context loss.

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 3 (Multi-Year Budget):** Carry-forward balance computation strategy and recurring expense year-scoping need validation. Edge cases around first-tracked-year and empty year handling.

**Phases with standard patterns (skip `/gsd-research-phase`):**
- **Phase 1 (Event Privacy):** Code exists, just needs hardening and testing.
- **Phase 2 (Reminder UI):** Backend complete, UI follows existing chip pattern, Google API constraints documented.
- **Phase 4 (YoY Comparison):** Architecture doc provides implementation spec, API design, and UI wireframe. Service reuses existing method.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Zero changes needed — all versions verified against requirements.txt and codebase |
| Features | HIGH | Feature inventory cross-referenced with existing schema, UI, and PROJECT.md requirements |
| Architecture | HIGH | All claims verified against actual source code; file paths, method names, and data flows confirmed |
| Pitfalls | HIGH | Each pitfall traced to specific code paths; Google API constraints verified via Context7 |

**Overall confidence:** HIGH

### Gaps to Address

- **Budget settings rate versioning:** Research recommends deferring year-scoped rates (document limitation with UI disclaimer). If users report confusion about changed past-year data, escalate to v2.2.
- **Sync error surfacing:** Silent exception swallowing in `sync_event_for_household` masks reminder and privacy sync failures. Not blocking for v2.1, but should be addressed soon.
- **`export_month` privacy tightening:** Currently safe because `_sync_recipients` filters, but data is loaded into memory unfiltered. Strengthen by passing `requesting_user_id` during privacy phase.
- **Empty year UX:** Navigating to years with no data should show a graceful empty state, not zeros. Needs design decision during Phase 3/4 planning.

## Sources

### Primary (HIGH confidence)
- `/googleapis/google-api-python-client` via Context7 — Calendar v3 Event.reminders spec: max 5 overrides, popup/email methods, 0–40320 minutes range
- Direct codebase analysis — models.py, schemas.py, repository.py, service.py, sync/service.py, routes.py, templates, JS, locale files

### Secondary (MEDIUM confidence)
- Google Calendar, Apple Calendar, Outlook, YNAB, Toshl — competitor/domain analysis for feature patterns and defaults

---
*Research completed: 2026-03-20*
*Ready for roadmap: yes*
