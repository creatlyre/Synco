# Feature Research: v2.1 — Privacy, Reminders & Multi-Year Budget

**Domain:** Household calendar — event privacy controls, reminder configuration, multi-year budget tracking
**Researched:** 2026-03-20
**Confidence:** HIGH
**Scope:** NEW features only — event visibility UI, reminder UI, multi-year budget browsing, YoY comparison. Existing features (event CRUD, recurring events, Google sync, budget tracker, NLP/OCR, i18n) already shipped through v2.0.

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist given the existing backend capabilities. Missing these = product feels broken or half-finished.

| Feature | Why Expected | Complexity | Dependencies on Existing |
|---------|--------------|------------|--------------------------|
| **Visibility toggle in event form** (shared/private) | Backend has `visibility` field + repo filtering since v1.1 schema; users expect UI control when capability exists | LOW | `EventCreate.visibility`, `EventUpdate.visibility` fields ✓; `_visible_to()` filter ✓ |
| **Private events hidden on partner's calendar** | Core privacy contract — marking private must hide entirely from partner | LOW | `EventRepository._visible_to()` ✓; `EventService` blocks edit/delete of others' private events ✓. Verify `requesting_user_id` flows through ALL calendar view routes. |
| **Lock icon or visual indicator for private events** | Users need confirmation their event is private; ambiguity erodes trust | LOW | Purely CSS/template. Owner sees lock badge; partner never sees event at all. |
| **Reminder on/off toggle in event form** | Backend syncs `effective_reminders` to Google Calendar; users expect to control what reminders fire | MEDIUM | `reminder_minutes_list` schema field ✓; `Event.effective_reminders` property ✓; `_event_body()` builds override payload ✓ |
| **Default reminder presets** (30 min + 2 days before) | Industry defaults: Google Calendar uses 30 min + 10 min. Household calendars need day-before reminders for family scheduling. | LOW | Pre-fill [30, 2880] when toggle is ON. Client-side defaults, no DB change. |
| **Year navigation in budget overview** (past years) | Year picker UI (`year-prev`/`year-next` buttons) already in budget_overview.html template; users expect it to work for all years | LOW | `overview_routes.py` accepts `year` query param ✓; `get_year_overview(calendar_id, year)` is year-agnostic ✓. May only need to remove frontend year restriction if one exists. |
| **Past year data display** | Users with budget data from previous years expect to browse it in the same dashboard | LOW | Same overview API/service works for any year. Key issue: `initial_balance` currently configured once in settings — needs year-awareness. |
| **YoY comparison summary** | Core ask — users need to see if they're doing better/worse than last year. Without this, multi-year browsing is just scroll exercise. | MEDIUM | Requires fetching two year overviews. New API endpoint or client-side computation. |

### Differentiators (Competitive Advantage)

Features that set the product apart for a household calendar+budget app. Not required, but high-value for low cost.

| Feature | Value Proposition | Complexity | Dependencies on Existing |
|---------|-------------------|------------|--------------------------|
| **Add/remove custom reminder entries** (up to 5) | Most simple calendars offer one reminder; letting users add up to 5 custom reminders (Google API max) feels powerful with minimal complexity | MEDIUM | Dynamic list UI: "Add reminder" button, each row = minutes input. Google API enforces max 5 overrides, 0–40320 minute range. `reminder_minutes_list` already stores the array. |
| **Reminder method choice** (popup vs email) | Google Calendar supports both `popup` and `email` notification methods; exposing this gives control over notification channel | LOW | Currently `_event_body()` hardcodes `"method": "popup"`. Needs method stored per-reminder in schema. Maps directly to Google API `overrides[].method`. |
| **Budget carry-forward balance** | Automatically compute end-of-year balance as next year's `initial_balance`, creating continuous financial timeline across years | MEDIUM | Compute Dec `account_balance` from year N → use as `initial_balance` for year N+1. Either store per-year or compute on the fly from first tracked year. |
| **YoY delta indicators** (arrows + percentages) | Color-coded arrows (green ↑ improvement, red ↓ decline) and percentage change in comparison view. At-a-glance financial health signal. | LOW | Pure presentation layer on top of two year-overview responses. Delta = (yearB - yearA) / yearA × 100. |
| **Private event indicator on month grid** | Small lock icon on event dots for owner in month grid view. Visual confirmation without needing to open event. | LOW | Conditionally render icon based on `visibility` field. Only visible to owner; partner never sees event entry at all. |
| **Reminder sync explanation in UI** | Helper text: "Reminders sync to Google Calendar on your phone." Avoids confusion about where notifications appear. | LOW | Text-only addition in event form. Prevents support burden. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems for this specific project.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **"Busy/Free" display for partner's private events** | Users may want to know partner is unavailable even if details hidden | Requires third visibility state, new UI for blocked time without details, complicates clean "hidden entirely" model. In 2-user household, time blocks reveal info anyway. | Keep binary: private = invisible. If partner needs to see blocked time, creator makes a vague shared event ("Busy"). |
| **In-app push notifications** (server-side reminders) | Users might expect CalendarPlanner itself to send reminders | Requires notification infrastructure (WebSocket/SSE/push service), persistent process, delivery guarantees — massive complexity for 2-user app | Rely on Google Calendar's notification system via sync. Reminders configured in CP sync to Google, which delivers to phone/email. This is the existing architecture. |
| **SMS reminders** | Google Calendar once supported SMS method | Google deprecated SMS reminders. Not available via Calendar API anymore. Attempting to send `"method": "sms"` will error. | Offer `popup` and `email` only — the two methods Google Calendar API v3 supports (HIGH confidence, Context7). |
| **Full budget history import** (Excel/CSV) | Users want to backfill years of financial data at once | Complex parsing, format validation, data mapping — high effort for one-time use. Edge cases with different column layouts. | Manual entry for past years. Already marked out-of-scope in PROJECT.md. |
| **Separate `initial_balance` settings per year** | Seems needed for multi-year support | Adds new DB table/schema, migration, per-year settings UI. Over-engineered when data already exists to compute it. | Carry-forward: year N+1 initial = year N final account_balance. Only first-ever year uses configured `initial_balance` from settings. |
| **Granular privacy levels** (default/public/private/confidential) | Google Calendar supports 4 visibility values | Two-user household doesn't need 4 levels. `confidential` = legacy alias for `private`. `public` meaningless with 2 users. More options = more confusion. | Binary: shared (both see) or private (only creator sees). Clean, unambiguous. |
| **Per-user default reminder preferences** (at this phase) | Set "my default reminders" once, auto-applied to all new events | Needs user preferences storage (new table/column), preference UI, default-application logic. Useful but adds scope beyond v2.1 target. | Use form-level defaults (30 min + 2 days) pre-filled when toggle is ON. Defer user-level preferences to v2.2+. |

## Feature Dependencies

```
[Visibility toggle in form]
    └──requires──> [visibility field in EventCreate/EventUpdate] (EXISTS ✓)
                       └──requires──> [_visible_to() repository filter] (EXISTS ✓)

[Private event filtering in all views]
    └──requires──> [requesting_user_id passed through view routes]
                       └──requires──> [EventService list methods accept requesting_user_id] (EXISTS ✓)

[Reminder toggle in form]
    └──requires──> [reminder_minutes_list in schema] (EXISTS ✓)
                       └──requires──> [Google sync _event_body() reminder payload] (EXISTS ✓)

[Custom reminder entries (add/remove)]
    └──requires──> [Reminder toggle in form]
    └──requires──> [reminder_minutes_list array field] (EXISTS ✓)

[Reminder method choice]
    └──requires──> [Custom reminder entries]
    └──requires──> [Schema change: store method per reminder] (NEW)

[Multi-year budget navigation]
    └──requires──> [year-parameterized overview API] (EXISTS ✓)
    └──requires──> [Budget carry-forward balance] (NEW)

[YoY comparison summary]
    └──requires──> [Multi-year budget navigation]
    └──requires──> [Fetch two year overviews simultaneously]

[YoY delta indicators]
    └──enhances──> [YoY comparison summary]

[Private event indicator on grid]
    └──enhances──> [Visibility toggle in form]
```

### Dependency Notes

- **Visibility toggle → existing backend:** Zero backend work. Toggle wires `visibility` field in form JS to existing schema. Repository filtering already enforces privacy.
- **Reminder toggle → existing sync:** `Event.effective_reminders` → `_event_body()` already builds Google API `reminders.overrides` payload. UI just needs to populate the `reminder_minutes_list` field.
- **Multi-year browsing → carry-forward:** The `initial_balance` in budget settings is a single value. For multi-year to work, year N+1 needs year N's ending balance. Must solve carry-forward before multi-year makes sense.
- **YoY comparison → multi-year navigation:** Must be able to display two years' data. Navigation is prerequisite, comparison is presentation.
- **Reminder method choice → schema change:** Currently `reminder_minutes_list` is `List[int]` (minutes only). To support method choice, needs `List[{method, minutes}]` or parallel `reminder_methods_list`. This is why method choice is P2 — it requires a schema migration.

## MVP Definition (v2.1 Milestone)

### Launch With (P1 — Must Have)

These directly map to the 4 active requirements in PROJECT.md:

- [ ] **Visibility toggle in event form** — Binary shared/private dropdown/toggle, wired to existing `visibility` field
- [ ] **Private event filtering verified in all view paths** — Audit that `requesting_user_id` flows through calendar_routes, day_events partial, month_grid partial
- [ ] **Reminder on/off toggle with defaults** — Toggle switch; when ON, pre-fill [30 min, 2 days] popup reminders; synced to Google via existing `_event_body()`
- [ ] **Multi-year budget navigation** — Ensure year picker has no frontend year restriction; backend already handles any year
- [ ] **Budget carry-forward balance** — Compute year N ending balance → year N+1 starting balance
- [ ] **YoY comparison summary** — Side-by-side annual totals (income, expenses, net balance) for selected year vs previous year

### Add After Validation (P2 — Should Have)

Enhancements to P1 features — ship if time allows in v2.1, otherwise v2.2:

- [ ] **Add/remove custom reminder entries** — Dynamic list UI for up to 5 reminders per event, minutes input per row
- [ ] **Visual private event indicator** — Lock icon on owner's event cards in day view and month grid
- [ ] **YoY delta indicators** — Color-coded arrows and ±% in comparison view
- [ ] **Reminder method choice** — Dropdown per reminder entry for popup vs email (requires schema migration for method storage)

### Future Consideration (P3 — Defer Beyond v2.1)

- [ ] **User-level default reminder preferences** — Auto-applied to new events. Needs preferences storage.
- [ ] **Budget data import (Excel/CSV)** — One-time historical import. High effort, already out-of-scope.
- [ ] **Busy/free time for private events** — Third visibility state. Over-engineered for 2-user household.
- [ ] **Per-year budget settings** — Separate initial_balance/rates per year. Carry-forward is simpler.

## Feature Prioritization Matrix

| Feature | User Value | Cost | Priority | Existing Backend |
|---------|------------|------|----------|------------------|
| Visibility toggle in form | HIGH | LOW | P1 | Schema ✓, Repo ✓ |
| Private event filtering (all views) | HIGH | LOW | P1 | Repo ✓, Service ✓ |
| Reminder toggle + defaults | HIGH | MEDIUM | P1 | Schema ✓, Sync ✓ |
| Multi-year budget navigation | HIGH | LOW | P1 | API ✓, Service ✓ |
| Budget carry-forward balance | HIGH | MEDIUM | P1 | Overview service ✓ |
| YoY comparison summary | HIGH | MEDIUM | P1 | Overview API ✓ |
| Custom reminder entries | MEDIUM | MEDIUM | P2 | Schema ✓ |
| Private event indicator | MEDIUM | LOW | P2 | Visibility toggle |
| YoY delta indicators | MEDIUM | LOW | P2 | YoY comparison |
| Reminder method choice | LOW | MEDIUM | P2 | Needs schema change |
| User default reminders | LOW | MEDIUM | P3 | — |
| Budget data import | LOW | HIGH | P3 | — |

## Competitor/Domain Analysis

### Event Privacy Patterns

| Aspect | Google Calendar | Apple Calendar | Outlook | CalendarPlanner v2.1 |
|--------|----------------|----------------|---------|----------------------|
| Visibility levels | `default`, `public`, `private`, `confidential` | Per-calendar only | `normal`, `personal`, `private`, `confidential` | `shared`, `private` (binary — right for 2-user household) |
| Private event display to others | Shows "Busy" time block, no details | N/A (calendar-level) | Shows "Private appointment" text | Completely hidden — simpler, more private for household |
| Default visibility | Calendar-level setting | N/A | Normal | `shared` (household default — sharing is the point) |
| UI control | Dropdown in event detail view | Per-calendar toggle | Dropdown | Toggle or dropdown in event form modal |

**Decision:** Binary shared/private. Google's 4 levels are for enterprise calendars with many viewers. Household needs only: "both see it" or "only I see it."

### Reminder Patterns

| Aspect | Google Calendar | Apple Calendar | Outlook | CalendarPlanner v2.1 |
|--------|----------------|----------------|---------|----------------------|
| Max reminders/event | 5 overrides | Unlimited | 2 | 5 (match Google API we sync to) |
| Methods | `popup`, `email` | Alert, email | Desktop toast, email, SMS | `popup`, `email` (match Google API) |
| Default reminders | 30 min + 10 min (calendar-level) | 15 min (app-level) | 15 min | 30 min + 2 days (household-oriented) |
| Minutes range | 0–40,320 (4 weeks max) | Flexible | Flexible | 0–40,320 (match Google API constraint) |
| Common presets | 5m, 10m, 15m, 30m, 1h, 1d, 2d, 1w | 5m, 15m, 30m, 1h, 1d | 0m, 5m, 15m, 30m, 1h, 1d, 1w | Preset dropdown: 15m, 30m, 1h, 1d, 2d, 1w |
| Notification delivery | Phone popup, email | iOS/macOS notification | Windows/mobile toast | Via Google Calendar sync to phone (architecture decision) |

**Decision:** Defaults of 30 min + 2 days (2880 min). The 2-day reminder is household-critical — doctor appointments, school events, etc. need advance planning notice. Google's 10-min default is too short for household scheduling. Delivery via Google Calendar sync — no need for CalendarPlanner-native push.

### Multi-Year Budget Patterns

| Aspect | YNAB | Mint/CreditKarma | Toshl | CalendarPlanner v2.1 |
|--------|------|-------------------|-------|----------------------|
| Year navigation | Monthly infinite scroll | Date range picker | Month picker + year dropdown | Year arrows (existing UI pattern) |
| Historical data | Full since onboarding | Bank-imported | Manual + import | Manual entry; carry-forward balance |
| Comparison | Month-to-month trends, category averages | Spending trends over time | Monthly/yearly reports | YoY annual summary (income, expenses, balance side-by-side) |
| Carry-forward | Automatic balances | Automatic via bank sync | Manual adjustment | Computed: year N end → year N+1 start |
| Empty year handling | Shows $0 categories | Not applicable (bank data) | Empty state | Show zeros with empty state message, no error |

**Decision:** Carry-forward computation, not per-year settings. Only the first tracked year uses `initial_balance` from budget settings. Subsequent years auto-compute from previous year's final `account_balance`. This matches YNAB's continuous balance model without bank sync complexity.

## Expected User Behaviors

### Privacy
- **Most events stay shared** — the whole point of a household calendar. Private events will be ~5-10% of total (surprise gifts, personal medical appointments).
- **Trust model:** Users expect private = truly invisible, not grayed out or "Busy" block. In 2-person household, any hint reveals information.
- **Common flow:** User creates event → remembers it's sensitive → switches toggle to private before saving. Or edits existing event to make it private.
- **Edge case:** User creates private recurring event — all occurrences must be private. Existing `_visible_to()` handles this since it filters by event visibility on the root.

### Reminders
- **"Set and forget" dominates:** ~80% of users will turn on reminders with defaults and never customize further. The toggle+defaults pattern serves this majority.
- **Power users want specificity:** Important events (doctor, school play, flight) get extra reminders (1 week + 1 day + 1 hour before). The add/remove UI serves this ~20%.
- **Phone delivery expectation:** Users expect notification on their phone. This works because reminders sync to Google Calendar, which handles mobile delivery. Without helper text explaining this, users may think reminders are broken.
- **Pitfall: "Where's my notification?"** If user doesn't have Google Calendar sync active, reminders configured in CP do nothing. Need sync status check or warning.

### Multi-Year Budget
- **Year switching is exploratory:** Users navigate to past years to check "what did we spend in 2025?" Quick arrow navigation is right — no need for date picker.
- **Comparison is the first instinct:** When viewing 2025, users immediately mentally compare to 2026. Surfacing YoY comparison automatically saves the mental effort.
- **Balance continuity is assumed:** If Dec 2025 ends with 15,000 PLN, users expect Jan 2026 to start there. Manual re-entry of initial balance per year = confusing.
- **Empty year navigation:** Going to 2020 (no data) should show zeros gracefully, not error or crash. "No data for this year" empty state.
- **First-time year navigation:** The year picker arrows already exist in the template. Users may not realize they can browse past years if there's a visual restriction. Removing the restriction is likely sufficient.

## Sources

- Google Calendar API v3 — Events resource: `visibility` supports `default`, `public`, `private`, `confidential` (Context7, HIGH confidence)
- Google Calendar API v3 — Reminders: max 5 overrides, methods `popup`/`email` only, 0–40,320 minutes range (Context7, HIGH confidence)
- Google Calendar API v3 — SMS method deprecated, not available (Context7, HIGH confidence)
- Existing codebase review — `EventCreate`/`EventUpdate` schemas with visibility + reminder fields (HIGH confidence)
- Existing codebase review — `EventRepository._visible_to()` filtering, `EventService` privacy enforcement (HIGH confidence)
- Existing codebase review — `Event.effective_reminders` property, `GoogleSyncService._event_body()` reminder sync (HIGH confidence)
- Existing codebase review — `OverviewService.get_year_overview(calendar_id, year)` year-agnostic API (HIGH confidence)
- Existing codebase review — budget_overview.html year picker with `year-prev`/`year-next` buttons (HIGH confidence)
| Complexity estimates | **MEDIUM** | Depends on implementation choices (framework, NLP service) |

---

## Sources

- **Cozi** (cozi.com): Market-leading family calendar; reverse-engineered feature set  
- **Google Calendar**: Public API documentation; feature parity analysis  
- **Apple Calendar / Family Sharing**: Public documentation  
- **Industry patterns**: Common household calendar use cases based on competitor analysis  

**Data sources:**
- Cozi feature overview: https://www.cozi.com/feature-overview/  
- Cozi calendar details: https://www.cozi.com/calendar/  
- Google Calendar creation & sharing: https://support.google.com/calendar/  

