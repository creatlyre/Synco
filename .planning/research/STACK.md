# Stack Research — v2.1 Additions

**Domain:** Event privacy, reminder UI, multi-year budget — additions to CalendarPlanner v2.1
**Researched:** 2026-03-20
**Confidence:** HIGH

## Key Finding: No New Dependencies Required

The existing stack fully supports all three v2.1 features. No new Python packages, no version upgrades, no new frontend libraries. This is a pure implementation milestone on existing infrastructure.

## Existing Stack (Verified Sufficient)

### Core Technologies

| Technology | Version | Purpose | Why Sufficient for v2.1 |
|------------|---------|---------|-------------------------|
| FastAPI | 0.135.1 | HTTP routing, dependency injection | Query params for year nav, existing route patterns cover all new endpoints |
| Pydantic | 2.10.6 | Schema validation | `EventCreate`/`EventUpdate` already validate `visibility`, `reminder_minutes_list` (0–40320 range), `Literal["shared", "private"]` |
| google-api-python-client | 2.93.0 | Google Calendar sync | Reminder overrides (max 5, popup/email, 0–40320 min) already implemented in `_event_body()`. ExtendedProperties carry `cp_visibility` |
| Jinja2 | 3.1.2 | Server-rendered templates | New UI sections (reminder editor, comparison table) are template additions only |
| Supabase (via httpx) | httpx 0.25.2 | Database storage | `events` table already has `visibility`, `reminder_minutes`, `reminder_minutes_list` columns. No schema migration needed |
| Tailwind CSS | Prebuilt 34KB | Styling | Existing utility classes cover all new UI elements. Rebuild with `npx @tailwindcss/cli` if new classes needed |

### Supporting Libraries (Already Present, No Changes)

| Library | Version | Relevance to v2.1 |
|---------|---------|-------------------|
| PyJWT | 2.8.0 | Auth unchanged — `requesting_user_id` already flows through `get_current_user` dependency |
| python-dateutil | 2.9.0 | Date math for year-over-year comparison (already imported) |
| pydantic-settings | 2.7.1 | `GOOGLE_EVENT_REMINDER_MINUTES` default (30) already in config — used as UI default |

## What Already Exists Per Feature

### 1. Event Privacy Controls — ~90% Complete

| Component | Status | What Exists |
|-----------|--------|-------------|
| Data model | ✅ Done | `Event.visibility: str = "shared"` in models.py |
| API schema | ✅ Done | `Literal["shared", "private"]` in EventCreate/EventUpdate |
| Repository filtering | ✅ Done | `_visible_to()` filters private events by `created_by_user_id` |
| Service enforcement | ✅ Done | Update/delete reject private events from non-owners |
| Event form UI | ✅ Done | Visibility dropdown in event_entry_modal.html |
| i18n keys | ✅ Done | `qa.visibility*` keys in both pl.json and en.json |
| Google Calendar sync | ✅ Done | `cp_visibility` in extendedProperties, `_extract_cp_visibility()` on import |
| Calendar view filtering | ⚠️ Verify | `requesting_user_id` param exists — confirm it's wired through calendar view routes |

**Stack need:** None. Implementation is wiring `requesting_user_id` through calendar view routes and adding a visual indicator (e.g., lock icon) for private events on the calendar grid.

### 2. Reminder UI Configuration — Backend Done, UI Missing

| Component | Status | What Exists |
|-----------|--------|-------------|
| Data model | ✅ Done | `Event.reminder_minutes`, `Event.reminder_minutes_list`, `effective_reminders` property |
| API schema | ✅ Done | Validated in EventCreate (0–40320 range, list support) |
| Google sync | ✅ Done | `_event_body()` builds `reminders.overrides` with popup method |
| Config default | ✅ Done | `GOOGLE_EVENT_REMINDER_MINUTES = 30` in Settings |
| Event form UI | ❌ Missing | No reminder fields in event_entry_modal.html or event_form.html |
| i18n keys | ❌ Missing | No reminder-related keys in locale files |

**Stack need:** None — pure template/JS work. Add reminder toggle + multi-reminder editor to event form.

**Google Calendar API constraints to respect in UI (verified via Context7, HIGH confidence):**
- Maximum **5 reminder overrides** per event
- Methods: `popup` (maps to phone notification) or `email`
- Minutes range: **0–40320** (0 min to 4 weeks)
- `useDefault: true` falls back to calendar-level defaults
- CalendarPlanner defaults to implement in UI: **30 minutes** + **2 days (2880 minutes)**

### 3. Multi-Year Budget Browsing — Already Functional

| Component | Status | What Exists |
|-----------|--------|-------------|
| Service | ✅ Done | `get_year_overview(calendar_id, year)` accepts any year |
| API | ✅ Done | `/api/budget/overview?year=YYYY` works for any integer year |
| Year navigation | ✅ Done | ← / → arrows in budget_overview.html with `currentYear--/++` |
| Year display | ✅ Done | `year-display` span updates on navigation |

**Stack need:** None. Year navigation already works. Consider adding URL query param (`?year=2025`) for bookmarkable state, but that's a UX enhancement, not a stack concern.

### 4. Year-over-Year Comparison — New Feature

| Component | Status | What's Needed |
|-----------|--------|---------------|
| Backend | 🆕 New endpoint | API to return two years' overview data in one response |
| Service | ⚠️ Reusable | Call `get_year_overview()` twice — no new logic needed |
| UI | 🆕 New template section | Side-by-side comparison table below main overview |
| i18n keys | 🆕 Missing | Comparison-related labels (PL + EN) |

**Stack need:** None. The existing `OverviewService.get_year_overview()` can be called for both years. No new computation library required — all math is addition/subtraction of already-computed yearly totals.

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| Vanilla JS reminder editor | Alpine.js for reactive form | Adding a JS framework for one form widget is overkill. The existing event form pattern (vanilla JS + event delegation) works and is consistent |
| Server-side comparison computation | Client-side JS fetch + compare | Keep compute server-side for consistency with existing overview pattern. Client fetches rendered data |
| `popup` as default reminder method | `email` reminders | Users want phone notifications via Google Calendar. `popup` maps to mobile push. `email` is secondary for household use |
| Reuse `get_year_overview()` twice | New comparison-specific SQL query | Two calls to existing function is simpler, tested, and maintainable. Data volume (12 months × 2 years) is trivial |
| Keep prebuilt Tailwind CSS | Switch to Tailwind runtime/CDN | Prebuilt approach was a v2.0 performance win (34KB vs 300KB). No reason to regress |

## What NOT to Add

| Avoid | Why | Do Instead |
|-------|-----|------------|
| Alpine.js / htmx / any JS framework | Adds build complexity for minimal gain. Existing vanilla JS + event delegation pattern is proven across the app | Continue vanilla JS pattern. The reminder editor is ~50 lines of JS |
| Chart.js / D3 for comparison visualization | Year-over-year is a summary table (4 rows × 2 columns). Charts are premature for 8 data points | HTML table with color-coded deltas (green/red), matching existing `colorClass()` pattern |
| Any ORM (SQLAlchemy, Tortoise) | Supabase REST API via httpx works. Adding an ORM now would require rewriting all repositories | Keep SupabaseStore pattern. No schema changes needed |
| Celery / background task runner | Sync is already synchronous per-request. Reminders are handled by Google Calendar, not CalendarPlanner | Google Calendar pushes notifications to phones. CalendarPlanner just sets the reminder config |
| WebSocket / SSE for live updates | Two-user household app. Page refresh on save is sufficient | Keep existing fetch + reload pattern |
| New pip packages of any kind | Zero new dependencies needed. Every feature builds on existing FastAPI + Pydantic + Google API + Jinja2 + Supabase | Leverage what's already installed |

## Installation

```bash
# No changes to requirements.txt
# No new packages needed

# Only action: rebuild Tailwind CSS if new utility classes are introduced
npx @tailwindcss/cli -i public/css/input.css -o public/css/style.css
```

## Version Compatibility

| Package | Current Version | Status | Notes |
|---------|-----------------|--------|-------|
| FastAPI | 0.135.1 | ✅ Current | No upgrade needed |
| Pydantic | 2.10.6 | ✅ Current | v2 features fully utilized |
| google-api-python-client | 2.93.0 | ✅ Sufficient | Calendar v3 API stable, reminder overrides supported |
| httpx | 0.25.2 | ✅ Sufficient | Supabase REST calls unchanged |
| Jinja2 | 3.1.2 | ✅ Current | Template inheritance working |

## Integration Points for Implementation

### Reminder UI → Google Calendar Sync Chain
```
Event Form (new UI) → EventCreate schema (existing validation)
  → EventRepository.create() (existing, stores reminder_minutes_list)
  → GoogleSyncService._event_body() (existing, builds overrides)
  → Google Calendar API (existing push sync)
  → Phone notification (Google handles this)
```

### Privacy Filtering Chain
```
Calendar View Route → EventService.list_month_expanded(requesting_user_id=user.id)
  → EventRepository._visible_to() (existing filter)
  → Template renders only visible events
  → Google Sync: cp_visibility in extendedProperties (existing)
```

### Year Comparison Data Flow
```
New API endpoint → OverviewService.get_year_overview(year_a) + get_year_overview(year_b)
  → Return combined response with delta calculations
  → Template renders side-by-side summary table
```

## Sources

- `/googleapis/google-api-python-client` via Context7 — Verified Calendar v3 Event.reminders spec: max 5 overrides, popup/email methods, 0–40320 minutes range (HIGH confidence)
- Codebase analysis — models.py, schemas.py, service.py, repository.py, sync/service.py, event_entry_modal.html, budget_overview.html, locale files (verified directly)
- requirements.txt — Current pinned versions confirmed
- config.py — `GOOGLE_EVENT_REMINDER_MINUTES = 30` default confirmed

---
*Stack research for: CalendarPlanner v2.1 — Privacy, Reminders & Multi-Year Budget*
*Researched: 2026-03-20*

