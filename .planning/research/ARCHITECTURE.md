# Architecture Research: v2.1 Feature Integration

**Domain:** Household calendar + budget planner — event privacy, reminder UI, multi-year budget
**Researched:** 2026-03-20
**Confidence:** HIGH (all findings verified against source code)

## Current System Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                     Jinja2 Templates + HTMX + JS                  │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │ calendar │  │ event_entry  │  │ budget_over  │  │ day_evts │  │
│  │  .html   │  │  _modal.html │  │  view.html   │  │  .html   │  │
│  └────┬─────┘  └──────┬───────┘  └──────┬───────┘  └────┬─────┘  │
├───────┴────────────────┴────────────────┴────────────────┴────────┤
│                    FastAPI Route Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐   │
│  │ events/      │  │ budget/      │  │ views/ + budget/*_views│   │
│  │  routes.py   │  │  *_routes.py │  │  calendar_routes.py    │   │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬───────────┘   │
├─────────┴──────────────────┴──────────────────────┴───────────────┤
│                    Service Layer                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐     │
│  │ EventService │  │ OverviewSvc  │  │  GoogleSyncService   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘     │
├─────────┴──────────────────┴────────────────────┴─────────────────┤
│                    Repository Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ EventRepo    │  │ ExpenseRepo  │  │ HoursRepo    │             │
│  │              │  │ EarningsRepo │  │ SettingsRepo │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
├─────────┴──────────────────┴────────────────┴─────────────────────┤
│                    SupabaseStore (httpx singleton)                 │
│  select / insert / update / delete → Supabase REST (PostgREST)    │
└───────────────────────────────────────────────────────────────────┘
```

### Existing Layer Pattern (all modules follow this)

```
routes.py       → FastAPI router, input validation, auth dependency
service.py      → Business logic, cross-repo coordination
repository.py   → SupabaseStore CRUD, row↔dataclass mapping
schemas.py      → Pydantic models for request/response
views.py        → HTML template rendering routes (Jinja2)
```

---

## Feature-by-Feature Integration Analysis

### Feature 1: Event Privacy Controls (Visibility Toggle)

**Status: ALREADY FULLY IMPLEMENTED — no new components needed**

The entire privacy pipeline is wired end-to-end across all layers:

| Layer | File | What Exists |
|-------|------|-------------|
| Model | `app/database/models.py` | `Event.visibility: str = "shared"` field |
| Schema | `app/events/schemas.py` | `visibility: Literal["shared", "private"]` on Create, Update, Response |
| Repository | `app/events/repository.py` | `_visible_to()` static method filters private events on all list queries |
| Service | `app/events/service.py` | Privacy guard in `update_event()` and `delete_event()` — returns "Event not found" for unauthorized access |
| Sync | `app/sync/service.py` | `_sync_recipients()` routes private events only to owner's Google Calendar; `_event_body()` stores `cp_visibility` in extended properties |
| UI Modal | `partials/event_entry_modal.html` | `<select id="event-entry-visibility">` with shared/private options + help text |
| UI Day View | `partials/day_events.html` | Passes `event.visibility` to `prefillEvent()` edit callback |
| JS Submit | `calendar.html` | `submitEventEntry()` includes `visibility` in POST/PUT payload; `prefillEvent()` restores select value on edit |
| i18n | `locales/en.json`, `pl.json` | `qa.visibility`, `qa.visibility_shared`, `qa.visibility_private`, `qa.visibility_help` keys |

**Conclusion:** This feature is complete. Validate with existing tests. No architecture changes needed.

---

### Feature 2: Reminder Configuration UI

**Status: Backend fully wired, UI controls missing — modify 3 existing files**

#### Existing Backend (complete, no changes needed)

| Layer | File | What Exists |
|-------|------|-------------|
| Model | `app/database/models.py` | `reminder_minutes: int \| None`, `reminder_minutes_list: list[int]`, `effective_reminders` property |
| Schema | `app/events/schemas.py` | `reminder_minutes_list: Optional[List[int]]` with boundary validation (0–40320 min = 4 weeks max) |
| Repository | `app/events/repository.py` | `create()` and `update()` read/write `reminder_minutes_list`; `_to_event()` maps from DB row |
| Sync | `app/sync/service.py` | `_event_body()` builds Google Calendar `reminders: { useDefault: false, overrides: [{method: "popup", minutes: N}] }` from `effective_reminders` |
| API | `app/events/routes.py` | `POST /api/events` and `PUT /api/events/{id}` accept `reminder_minutes_list` in JSON body |

#### Missing: UI Layer Only (3 files to modify)

**1. `app/templates/partials/event_entry_modal.html`** — Add reminder section to the form:
- Toggle checkbox: "Reminders" / "Przypomnienia"
- When toggled ON: render default chips (30 min + 2880 min / 2 days)
- Each chip: removable pill with `✕` button
- "Add reminder" button opens inline select/input for custom value
- Place after the visibility field, before the recurrence fields

**2. `app/templates/calendar.html`** (JS section) — Wire reminder data into existing flow:
- `submitEventEntry()`: collect reminder values from chips, include `reminder_minutes_list: [30, 2880]` in payload
- `prefillEvent()`: accept `reminder_minutes_list` parameter, populate chips when editing existing event
- `resetEventEntryForm()`: clear reminder chips
- New helper: `addReminderChip(minutes)`, `removeReminderChip(index)`, `getReminderList()`

**3. `app/templates/partials/day_events.html`** — Show reminder indicator (optional, low priority):
- Small 🔔 icon or text when `event.effective_reminders` is non-empty

#### Data Flow (unchanged API contract)

```
User toggles reminders ON → default chips appear [30min, 2 days]
User adds/removes chips → UI state updates
User clicks Save → submitEventEntry()
  → POST/PUT /api/events { ..., reminder_minutes_list: [30, 2880] }
    → EventService.create_event() / EventRepository.create()
      → INSERT/UPDATE in Supabase events table
    → GoogleSyncService.sync_event_for_household()
      → _event_body() reads effective_reminders
      → Google Calendar API: reminders.overrides = [{popup, 30}, {popup, 2880}]
```

**No database migration.** Column `reminder_minutes_list` (JSONB array) already exists in events table.
**No new Python files.** Backend API already accepts and processes the data.

---

### Feature 3: Multi-Year Budget Browsing

**Status: Core functionality already works — verify and refine UX**

#### What Already Works

| Component | File | Status |
|-----------|------|--------|
| API endpoint | `app/budget/overview_routes.py` | `GET /api/budget/overview?year=N` — accepts any integer year |
| Service | `app/budget/overview_service.py` | `get_year_overview(calendar_id, year)` — fully year-parameterized |
| Expense repo | `app/budget/expense_repository.py` | `get_by_calendar_year(calendar_id, year)` — queries by year + unions recurring (month=0) |
| Income repos | `app/budget/income_repository.py` | `get_by_calendar_year(calendar_id, year)` — queries by year |
| Year picker UI | `app/templates/budget_overview.html` | `year-prev`/`year-next` buttons, `currentYear` JS state, fully event-wired |
| Year display | `app/templates/budget_overview.html` | `#year-display` updates on navigation, `reload()` re-fetches and re-renders |

#### Architecture Concern: BudgetSettings Not Year-Scoped

`BudgetSettings` has one row per `calendar_id` with `rate_1`, `rate_2`, `rate_3`, `zus_costs`, `accounting_costs`, `initial_balance` — **no year column**. Viewing past years applies current rates retroactively.

| Approach | Complexity | Accuracy | Recommendation |
|----------|-----------|----------|----------------|
| A: Keep single settings, document limitation | None | Approximate for past years | **Use this for v2.1** |
| B: Add `year` column to BudgetSettings | DB migration + per-year UI | Historically accurate | Defer to v3+ if users request it |

**Decision: Approach A.** The core multi-year navigation already works. The rates issue is an edge case (rates rarely change for this household use case). Document it in the UI with a note like "Calculations use current rates."

#### Modifications Needed

**1. `app/templates/budget_overview.html`** — Minor UX polish:
- Highlight current year in the year picker (bold/distinctive styling)
- Optional: limit backward navigation to a sensible range (e.g., current year − 5)

**2. Income/Expense view pages** — Verify year consistency:
- Check if `budget_income.html` and `budget_expenses.html` handle year navigation
- If they hardcode current year, add year param support to match overview

**No new Python files. No database migration.**

---

### Feature 4: Year-over-Year Summary Comparison

**Status: COMPLETELY NEW — extend 3 existing files**

This feature requires a new service method, a new API endpoint, and a new UI section. All added to existing files.

#### Components to Add

| Type | File to Modify | What to Add |
|------|---------------|-------------|
| Service method | `app/budget/overview_service.py` | `get_year_comparison(calendar_id, years: list[int])` |
| API endpoint | `app/budget/overview_routes.py` | `GET /api/budget/overview/compare?years=2025,2026` |
| UI section | `app/templates/budget_overview.html` | Comparison panel below the main overview table |
| i18n keys | `app/locales/en.json`, `pl.json` | Comparison labels |

#### Service Method Design

```python
# In overview_service.py — reuses existing get_year_overview()
def get_year_comparison(self, calendar_id: str, years: list[int]) -> dict:
    summaries = []
    for year in sorted(years):
        overview = self.get_year_overview(calendar_id, year)
        months = overview["months"]
        summaries.append({
            "year": year,
            "total_net": round(sum(m["net"] for m in months), 2),
            "total_additional": round(sum(m["additional_earnings"] for m in months), 2),
            "total_recurring_expenses": round(sum(m["recurring_expenses"] for m in months), 2),
            "total_onetime_expenses": round(sum(m["onetime_expenses"] for m in months), 2),
            "total_balance": round(sum(m["monthly_balance"] for m in months), 2),
            "final_account_balance": months[-1]["account_balance"] if months else 0,
            "initial_balance": overview["initial_balance"],
        })
    return {"summaries": summaries}
```

**Key design decision:** Reuse `get_year_overview()` rather than duplicating calculation logic. Each call makes ~4 DB queries (settings, hours, earnings, expenses), so comparing 2–3 years = 8–12 queries total. Acceptable for this two-user app.

#### API Endpoint Design

```python
# In overview_routes.py — parse comma-separated years, cap at 5
@router.get("/compare")
async def compare_years(
    years: str = Query(...),
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    year_list = [int(y) for y in years.split(",") if y.strip().isdigit()][:5]
    if len(year_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 years required")
    service = _service(db)
    data = service.get_year_comparison(user.calendar_id, year_list)
    return {"data": data}
```

**Note:** Register this endpoint BEFORE the parameterized `/compare` won't conflict with existing routes since there's no `GET /api/budget/overview/{param}` pattern.

#### UI Design

Comparison renders as an expandable section below the year overview table:

```
[← 2025 →]                              [Compare ▼]

| Month | Net | Additional | Rec.Exp | One-time | Balance | Account |
|-------|-----|------------|---------|----------|---------|---------|
| Jan   | ... | ...        | ...     | ...      | ...     | ...     |
...

── Year Comparison ────────────────────────────────────────
| Year | Net Income | Additional | Expenses | Balance | Final Account |
|------|------------|------------|----------|---------|---------------|
| 2025 | 120,000    | 5,000      | 80,000   | 45,000  | 95,000        |
| 2026 | 130,000    | 6,000      | 85,000   | 51,000  | 146,000       |
| Δ    | +10,000    | +1,000     | +5,000   | +6,000  | +51,000       |
```

The comparison button toggles this section. By default it compares current year with previous year. Color-code deltas: green for improvements, red for regressions.

#### Data Flow

```
User clicks "Compare" → JS fetches comparison
  → GET /api/budget/overview/compare?years=2025,2026
    → OverviewService.get_year_comparison()
      → get_year_overview(cal_id, 2025)  # reuses existing
      → get_year_overview(cal_id, 2026)  # reuses existing
      → aggregates totals, returns summaries
    → Returns { summaries: [{year: 2025, ...}, {year: 2026, ...}] }
  → JS renders comparison table with delta row
```

---

## Summary: New vs Modified Components

| Feature | New Files | Modified Files | DB Migration |
|---------|-----------|----------------|--------------|
| Event privacy | 0 | 0 (already complete) | None |
| Reminder UI | 0 | 3 (modal HTML, calendar JS, day events HTML) | None |
| Multi-year budget | 0 | 1–3 (overview HTML, possibly income/expense views) | None |
| YoY comparison | 0 | 3 (overview_service.py, overview_routes.py, overview HTML) | None |
| i18n keys | 0 | 2 (en.json, pl.json) | None |

**Total: 0 new files created, 5–7 existing files modified, 0 database migrations.**

### i18n Additions Required

Both `app/locales/en.json` and `app/locales/pl.json` need keys for:

- **Reminder UI:** toggle label, default reminder descriptions (e.g., "30 minutes", "2 days"), add button, chip display format
- **Comparison UI:** compare button label, table headers, delta row label, "no data" state
- **Budget year note:** "Calculations use current rates" disclaimer (if shown)

---

## Recommended Build Order

Dependencies determine the sequence:

```
Phase 1: Event Privacy (tests only — validate existing implementation)
  └── Depends on: nothing
  └── Risk: LOW — code reviewed, appears complete

Phase 2: Reminder UI (frontend wiring to existing backend)
  └── Depends on: nothing new in backend
  └── Touches: event_entry_modal.html, calendar.html JS, day_events.html
  └── Risk: LOW — backend contract is stable

Phase 3: Multi-Year Budget Browsing (verify/polish existing)
  └── Depends on: nothing new
  └── Touches: budget_overview.html (minor UX), verify income/expense views
  └── Risk: LOW — year picker already functional

Phase 4: Year-over-Year Comparison (new service + API + UI)
  └── Depends on: multi-year browsing working correctly (Phase 3)
  └── Touches: overview_service.py, overview_routes.py, budget_overview.html
  └── Risk: MEDIUM — new API endpoint, new JS rendering
```

**Phase ordering rationale:**
1. Privacy first — zero effort if already done, just validate.
2. Reminders — self-contained frontend task, backend ready, clears the event feature work.
3. Multi-year browsing — must work correctly before comparison builds on top of it.
4. YoY comparison — highest complexity, uses `get_year_overview()` which must be solid for arbitrary years.

---

## Patterns to Follow

### Pattern: Chip-Based Multi-Value Input (Reminders)

Match existing glass UI design system. Use removable pill/chip components:

```html
<div id="reminder-chips" class="flex flex-wrap gap-1">
  <span class="rounded-full bg-white/10 px-2 py-0.5 text-xs border border-white/20">
    30 min <button class="ml-1 opacity-60 hover:opacity-100">✕</button>
  </span>
</div>
```

Consistent with the date badge style in `day_events.html` (`rounded-full bg-white/10 px-3 py-1 text-xs`).

### Pattern: Reuse Service Methods for Aggregation

Don't duplicate budget calculation logic. The comparison endpoint calls `get_year_overview()` per year:

```python
# Good: reuse
summaries = {y: self.get_year_overview(cal_id, y) for y in years}

# Bad: copy-paste monthly calculation loop into comparison method
```

### Pattern: Follow Existing Budget JS Structure

The budget overview uses an IIFE with internal `currentYear` state, `reload()` function, and event delegation. The comparison UI should follow the same pattern — add to the existing IIFE, not a separate script block.

---

## Anti-Patterns to Avoid

### Anti-Pattern: Year-Scoped BudgetSettings in v2.1

Adding a `year` column to `BudgetSettings` would cascade into:
- Database migration
- Settings UI showing year selector ("which year's rates am I editing?")
- Backfill logic for existing data
- Every budget query needing year-aware settings lookup
- Income calculation engine changes

Excessive for v2.1. Defer if historical rate accuracy becomes a real user need.

### Anti-Pattern: Separate Comparison Page

Don't create `/budget/comparison` with a new template. Keep it as an expandable section in `budget_overview.html`. Avoids:
- New sidebar link and navigation complexity
- Template duplication
- State sync between pages (which year is selected where?)

### Anti-Pattern: Reminder Defaults in Database

Default reminders (30 min + 2 days) should be UI-only defaults populated by JavaScript when the toggle is turned on. Don't add a user preferences table for reminder defaults. If a user unchecks reminders, send `reminder_minutes_list: []`.

### Anti-Pattern: Creating New Reminder Service/Repository

The reminder data is part of the Event model. No separate `ReminderService` or `ReminderRepository` — it flows through the existing `EventService` → `EventRepository` pipeline. The `reminder_minutes_list` is just another field on the event.

---

## Scalability Considerations

| Concern | Current (2 users) | Notes |
|---------|-------------------|-------|
| Comparison API | 2–3 calls to `get_year_overview()` per request (~8–12 DB queries) | Acceptable; add caching only if >5 years compared |
| Reminder storage | JSONB array column on events table | Fine for any reasonable reminder count per event |
| Year navigation | Unbounded year picker | Limit to current year ± 10 in UI for UX |
| Privacy filtering | In-memory filter via `_visible_to()` after full table load | Fine for household scale (~hundreds of events); add PostgREST filter if event count grows significantly |
| Budget year queries | 4 DB round-trips per year view | Acceptable; batch into single RPC if latency becomes an issue |

## Sources

- Direct codebase analysis: all model, schema, repository, service, route, template, and JS files reviewed
- Existing patterns verified against v1.0–v2.0 implementation
- Confidence: HIGH — all claims verified against actual source code
