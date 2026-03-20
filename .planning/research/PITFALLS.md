# Pitfalls Research

**Domain:** Adding event privacy, reminder UI, and multi-year budget to existing household calendar
**Researched:** 2026-03-20
**Confidence:** HIGH — based on direct codebase analysis and Google Calendar API documentation

---

## Critical Pitfalls

### Pitfall 1: Visibility change doesn't clean up partner's Google Calendar

**What goes wrong:**
When an event changes from `shared` to `private`, `sync_event_for_household` correctly limits `_sync_recipients` to just the owner — but the event _already exists_ in the partner's Google Calendar from a prior sync. The partner continues to see the now-private event indefinitely.

**Why it happens:**
The sync service only handles the push-forward case (who gets the event now), not the cleanup case (who had it before and shouldn't anymore). The current `_sync_recipients` method filters recipients for the current sync, but doesn't compute the delta — users who were recipients but no longer are.

**How to avoid:**
When visibility changes from `shared` to `private`: (1) identify household users who are NOT the owner, (2) find and delete the event from their Google Calendars. Add a `_retract_from_non_recipients` step in `sync_event_for_household` that runs when `cp_visibility` extended property differs from the event's current visibility.

**Warning signs:**
- Partner still sees private events on their phone after sync
- Only the web UI filters correctly; Google Calendar shows stale state
- No `events().delete()` call path exists for visibility-change scenarios

**Phase to address:**
Event privacy phase — must ship alongside the visibility toggle, not as a follow-up.

---

### Pitfall 2: `export_month` syncs private events through the full pipeline

**What goes wrong:**
`export_month` in `app/sync/service.py` calls `service.list_month_expanded(user.calendar_id, year, month)` **without** `requesting_user_id`. This returns ALL events including the partner's private ones. Each event then goes through `sync_event_for_household`, where `_sync_recipients` correctly filters — but the full event object (including private titles and descriptions) is loaded into memory and passed through the pipeline before filtering.

**Why it happens:**
`export_month` was written before privacy existed. It bulk-fetches all calendar events, relying on downstream `_sync_recipients` for filtering. The filtering is correct for who receives the push, but the data is already loaded.

**How to avoid:**
This is currently safe because `_sync_recipients` prevents the push. However: (1) Never add logging/debugging that dumps event bodies before the recipient filter. (2) If adding batch operations, always filter events BEFORE constructing payloads. (3) Consider passing `requesting_user_id` to `list_month_expanded` in `export_month` so each user only iterates over events they should see.

**Warning signs:**
- Private event titles appearing in server logs
- Debug middleware exposing event bodies to response headers
- Adding a sync report feature that lists all synced event titles

**Phase to address:**
Event privacy phase — tighten `export_month` to filter per-user before sync loop.

---

### Pitfall 3: Initial balance is not year-scoped — multi-year running balance starts wrong

**What goes wrong:**
`BudgetSettings.initial_balance` is a single float value per calendar. The `get_year_overview` service uses it as the starting balance for ANY year requested. Navigating to 2024 uses the same initial balance as 2026, producing incorrect running balances for every past and future year.

**Why it happens:**
Budget was designed as current-year-only. The initial balance was intended as account balance at start of this year. Extending to multi-year without computing year-start balances from the prior year's ending balance creates incorrect data.

**How to avoid:**
For year Y, the starting balance should be: `initial_balance + sum of monthly_balance for every month in years before Y`. Two approaches:
1. **Compute dynamically**: When loading year Y overview, first calculate ending balance of year Y-1 (recursively). Cache aggressively.
2. **Snapshot yearly**: Store a `year_opening_balance` table with one row per calendar per year. Recompute when prior year data changes.

Option 1 is simpler for a two-user household app with limited history depth.

**Warning signs:**
- Year overview shows same starting balance regardless of which year is selected
- Running balance in 2025 doesn't match ending balance of 2024
- Users report budget seems wrong for previous years

**Phase to address:**
Multi-year budget phase — must fix before enabling year navigation.

---

### Pitfall 4: Recurring expenses appear in all years regardless of when created

**What goes wrong:**
`ExpenseRepository.get_by_calendar_year` fetches recurring expenses (`month=0`) with a query that has no year filter: `{"calendar_id": ..., "month": "eq.0"}`. A recurring expense created in 2026 appears when viewing 2024, even though it didn't exist then.

**Why it happens:**
Recurring expenses were designed as same every month, same every year for the current-year-only model. The `year` field on recurring expenses is set to creation year but never used for filtering — the query ignores it.

**How to avoid:**
Two options:
1. **Add effective date range**: Add `effective_from_year` and optional `effective_until_year` fields to expenses. Filter recurring expenses where `effective_from_year <= requested_year`.
2. **Filter by creation year**: For recurring rows, filter `year <= requested_year` meaning this is the first year they apply.

Option 2 is simpler but requires the `year` field on recurring expenses to mean first year this applies.

**Warning signs:**
- Viewing past years shows expenses that didn't exist yet
- Year-over-year comparison shows identical recurring expense totals for years before the user even started tracking
- Deleting a recurring expense removes it from all historical years too

**Phase to address:**
Multi-year budget phase — resolve before shipping year navigation.

---

### Pitfall 5: Budget settings (rates, ZUS, accounting) are not year-versioned

**What goes wrong:**
`BudgetSettings` stores a single set of rates per calendar. If hourly rates change from 2025 to 2026, viewing the 2025 overview uses the current (2026) rates — retroactively changing all 2025 calculations. Year-over-year comparison becomes meaningless because both years use identical rates.

**Why it happens:**
Settings were designed as current configuration for single-year use. No historical versioning was needed.

**How to avoid:**
Two approaches:
1. **Year-scoped settings**: Add a `year` column to `budget_settings` or create a `budget_settings_yearly` table. Each year has its own rates. When navigating to a new year for the first time, copy forward from the previous year.
2. **Settings changelog**: Store settings changes with timestamps and compute the effective settings for any given year. Over-engineered for this use case.

Option 1 is recommended. A copy-forward mechanism when the user first navigates to a new year provides a natural workflow.

**Warning signs:**
- Changing current year rates retroactively alters past year summaries
- Year-over-year comparison shows identical gross income with identical rates
- Users confused why past year data changed

**Phase to address:**
Multi-year budget phase — core data model change, must precede year-over-year comparison.

---

### Pitfall 6: Google Calendar API rejects more than 5 reminder overrides

**What goes wrong:**
The Google Calendar API enforces a maximum of 5 reminder overrides per event. The current Pydantic schema validates each reminder is 0–40320 minutes but does not validate the list length. If the UI allows adding 6+ reminders, `events().insert()` or `events().update()` throws a 400 error, and the event fails to sync silently (caught by the generic `except Exception` in `sync_event_for_household`).

**Why it happens:**
The backend validation was written for the reminder data model (valid minute ranges) without consulting the Google Calendar API constraint on list length. The sync service catches all exceptions, so the failure is invisible to the user.

**How to avoid:**
1. Add `max_length=5` validation on `reminder_minutes_list` in `EventCreate` and `EventUpdate` schemas.
2. Surface sync errors to the user rather than silently swallowing them.
3. In the UI, disable add reminder button after 5 entries.

**Warning signs:**
- Sync reports showing errors like invalid value for reminders
- Events with 6+ reminders sync successfully to CP but never appear in Google Calendar
- Users report reminders work in browser but not on phone

**Phase to address:**
Reminder UI phase — enforce limit in schema AND UI simultaneously.

---

## Moderate Pitfalls

### Pitfall 7: Dual reminder fields create ambiguous state

**What goes wrong:**
The `Event` model has both `reminder_minutes` (single int, legacy) and `reminder_minutes_list` (list[int], new). The `effective_reminders` property provides fallback logic (prefer list, then single, then empty). If the UI writes to `reminder_minutes_list` but old code or imports write to `reminder_minutes`, events end up with both fields set, and the behavior depends on which the `effective_reminders` property prioritizes.

**Why it happens:**
`reminder_minutes` was the v1.1 backend-only field. `reminder_minutes_list` was added for multi-reminder support. Both coexist without a clear migration path.

**How to avoid:**
1. UI should exclusively write to `reminder_minutes_list` and set `reminder_minutes = None` when saving.
2. On import from Google Calendar, populate only `reminder_minutes_list`.
3. Add a one-time migration to move any existing `reminder_minutes` values into `reminder_minutes_list` and null out the single field.

**Warning signs:**
- Event has `reminder_minutes=30` AND `reminder_minutes_list=[60, 1440]` — which reminder set does the user get?
- Editing an event in UI shows different reminders than what syncs to Google
- Import/export round-trip changes reminder values

**Phase to address:**
Reminder UI phase — resolve before shipping the UI, as users will be confused by phantom reminders.

---

### Pitfall 8: Private event import from Google doesn't enforce ownership

**What goes wrong:**
`_upsert_google_event` creates new events with `visibility: self._extract_cp_visibility(google_event)` from extended properties. But the import runs as the importing user, so `created_by_user_id` is set to whoever triggers the import. If User B imports and a private event from User A comes through via a shared Google Calendar, it gets created with `created_by_user_id = User B` — now User B owns a private event that was supposed to be hidden from them.

**Why it happens:**
The import path was designed before privacy. It attributes all imported events to the importing user. Extended properties are private in Google's sense (app-scoped), but the `cp_owner_id` field is only used in the sync body, not validated on import.

**How to avoid:**
1. On import, check `cp_owner_id`: if the extended property exists and doesn't match the importing user, skip the event (it's someone else's private event).
2. Never import events with `cp_visibility=private` unless `cp_owner_id` matches the importing user.
3. If no extended properties exist (external events), default to `shared`.

**Warning signs:**
- User B imports and suddenly owns User A's private events
- Private events appear as created by the wrong user
- Circular sync: User A creates private event → syncs to Google → User B imports → now both see it

**Phase to address:**
Event privacy phase — must be fixed together with the visibility toggle.

---

### Pitfall 9: No reminders-disabled vs use-defaults distinction in UI

**What goes wrong:**
The reminders system has three meaningful states: (1) use defaults (30 min + 2 days), (2) custom reminders, (3) no reminders. The `effective_reminders` property returns `[]` for both no reminders explicitly set and never configured. In Google Calendar, `useDefault: true` and `useDefault: false, overrides: []` are different behaviors.

**Why it happens:**
The backend maps empty reminders to `useDefault: true` (Google Calendar defaults). The UI needs a way to say I explicitly want NO reminders which requires `useDefault: false, overrides: []`. There's no field for this distinction.

**How to avoid:**
Add a `reminders_enabled` boolean (or a `reminder_mode` enum: `default`, `custom`, `none`) to the Event model. The UI toggle maps to this field:
- Toggle OFF → `reminder_mode = none` → sync with `useDefault: false, overrides: []`
- Toggle ON + empty list → `reminder_mode = default` → sync with `useDefault: true`
- Toggle ON + custom list → `reminder_mode = custom` → sync with overrides

**Warning signs:**
- Users toggle no reminders but still get default Google Calendar notifications
- Toggling reminders on shows empty list instead of defaults
- Round-trip through sync changes reminder behavior

**Phase to address:**
Reminder UI phase — define the tri-state before building the toggle component.

---

### Pitfall 10: Year-over-year comparison with missing data shows misleading zeros

**What goes wrong:**
Viewing a comparison between 2026 (with data) and 2024 (no data) shows 2024 as all zeros — identical to user tracked nothing vs user earned nothing. Users can't distinguish between I didn't enter data and there was no income.

**Why it happens:**
The overview service returns `{ net: 0, additional_earnings: 0, ... }` for months with no data. There's no concept of no data recorded vs data recorded as zero.

**How to avoid:**
1. Track which months have been touched (have any hours or expenses entered).
2. In the comparison view, show a distinct state for months with no data (e.g., dash or No data) vs months with explicit zeros.
3. Check if `MonthlyHours` rows exist for that month to determine if data was entered.

**Warning signs:**
- Comparison shows 2024 with identical zeroes across all months
- Users interpret 0 as I earned nothing rather than I didn't track
- Historical comparison suggests dramatic income changes that are actually data gaps

**Phase to address:**
Year-over-year comparison phase — distinguish empty from zero in the comparison UI.

---

### Pitfall 11: Event form doesn't populate visibility/reminders when editing existing events

**What goes wrong:**
The event entry modal has a visibility `<select>` but the JavaScript that populates the form for editing (pre-filling fields from existing event data) may not set visibility or reminder fields. The user opens an existing private event for editing, sees shared selected (the default), saves, and the event silently becomes shared.

**Why it happens:**
The form template exists but the populate/edit JavaScript path needs to read `visibility` and `reminder_minutes_list` from the API response and set the form controls. If this mapping is missed, defaults overwrite existing values.

**How to avoid:**
1. When populating the edit form, always read `visibility` from the event response and set the `<select>` value.
2. For reminders, populate the reminder list UI from `reminder_minutes_list` in the event response.
3. Add an integration test: create private event → open edit form → save without changes → verify still private.

**Warning signs:**
- Editing a private event and saving without changing anything makes it shared
- Editing an event with custom reminders resets them to defaults
- No test coverage for the edit-and-save-unchanged round-trip

**Phase to address:**
Both event privacy and reminder UI phases — the form population logic is shared.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Single `BudgetSettings` row for all years | No schema migration needed | Can't compare years accurately; rate changes rewrite history | Never — must fix for multi-year |
| Both `reminder_minutes` and `reminder_minutes_list` fields | Backwards compat with v1.1 | Ambiguous state, dual code paths, confusion in sync | Only during migration; deprecate single field within this milestone |
| Recurring expenses with no year scope | Simple model for current-year view | Historical views show future recurring costs | Never for multi-year — corrupt historical data |
| Swallowing sync exceptions silently | Sync never fails from user perspective | Users don't know their reminders or privacy didn't sync | Acceptable short-term; add user-facing sync status feedback soon |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Google Calendar — Reminders | Allowing >5 overrides (API rejects silently when caught) | Enforce max 5 in schema AND UI; surface sync errors |
| Google Calendar — Private events | Syncing private event to all users, relying only on `_sync_recipients` | Must also DELETE from ineligible users' calendars on visibility change |
| Google Calendar — Import | Importing private events and setting `created_by_user_id` to importer | Validate `cp_owner_id` extended property; skip events owned by other users |
| Google Calendar — Reminder methods | Only using `popup` method; Google also supports `email` | Document that only popup is supported; consider email as future option |
| Supabase — Recurring expense query | Fetching `month=0` without year filter returns ALL recurring expenses across years | Add year-scoping to recurring expense queries |
| Supabase — Budget settings | Single settings row means UPDATE affects all year views | Version settings per year or snapshot on year transition |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Computing year-start balance by replaying all prior years | Slow page load when navigating to distant past years | Cache or snapshot yearly opening balances | When budget history exceeds ~5 years |
| `_all_active_for_calendar` fetching ALL events for privacy filtering | Slow calendar views as event count grows | Push visibility filter into Supabase query (add `or` filter for visibility=shared OR created_by_user_id=requesting_user) | When calendar exceeds ~500 events |
| Year-over-year comparison querying two full years of data | Double the budget queries per page load | Parallel fetch both years; consider a summary/aggregate table | Noticeable if budget data grows significantly per year |
| Sync cleanup scanning all household users' Google Calendars on visibility change | Slow save when changing visibility | Batch calendar cleanup; run async if possible | Always slow (Google API round-trips) but acceptable for rare visibility changes |
