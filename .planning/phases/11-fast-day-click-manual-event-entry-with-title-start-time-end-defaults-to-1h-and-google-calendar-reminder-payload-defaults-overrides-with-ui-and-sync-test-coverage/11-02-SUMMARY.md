---
phase: 11-fast-day-click-manual-event-entry-with-title-start-time-end-defaults-to-1h-and-google-calendar-reminder-payload-defaults-overrides-with-ui-and-sync-test-coverage
plan: 02
subsystem: sync
tags: [google-calendar, reminders, dataclass, pydantic, backward-compat]

requires:
  - phase: 11-01
    provides: "Day-click quick-entry UI with auto-calculated end-time"
provides:
  - "Event model with reminder_minutes_list field and effective_reminders property"
  - "EventCreate/EventUpdate/EventResponse schemas with reminder input validation"
  - "Google sync payload with multi-reminder overrides array"
  - "Tests for default, single, multiple, and precedence reminder scenarios"
affects: [11-03, ui-reminder-form, future-notification-preferences]

tech-stack:
  added: []
  patterns: ["backward-compat dual-field with property accessor (reminder_minutes + reminder_minutes_list → effective_reminders)"]

key-files:
  created: []
  modified:
    - app/database/models.py
    - app/events/schemas.py
    - app/events/repository.py
    - app/sync/service.py
    - tests/test_sync_api.py

key-decisions:
  - "Backward-compat dual-field approach: keep reminder_minutes, add reminder_minutes_list with effective_reminders property"
  - "No config fallback in _event_body: empty reminders → useDefault=True (Google handles its own defaults)"
  - "Replaced SimpleNamespace with Event dataclass in _event_body tests for property support"

patterns-established:
  - "Dual-field backward compat: old single field + new list field + property accessor for unified access"

requirements-completed: []

duration: 5min
completed: 2026-03-20
---

# Phase 11 Plan 02: Reminder Infrastructure Summary

**Multi-reminder support via backward-compat dual-field model with Google Calendar overrides array and 4 new payload tests**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-20T09:55:28Z
- **Completed:** 2026-03-20T10:00:28Z
- **Tasks:** 4/4
- **Files modified:** 5

## Accomplishments
- Extended Event dataclass with `reminder_minutes_list` and `effective_reminders` property (fallback chain: list → single → empty)
- Added reminder fields to EventCreate/EventUpdate/EventResponse with validation (non-negative, max 4 weeks)
- Rewrote `_event_body` to generate Google `reminders.overrides[]` from `effective_reminders`
- Added 4 new tests (default, single, multiple, precedence) and updated 2 existing visibility tests to use Event dataclass

## Task Commits

1. **Task 1: Extend Event model with reminder support** - `4d59b8f` (feat)
2. **Task 2: Update schemas with reminder fields** - `52a5a7b` (feat)
3. **Task 3: Update sync service for multi-reminder payload** - `857f85c` (feat)
4. **Task 4: Add reminder payload tests** - `7374563` (test)

## Files Created/Modified
- `app/database/models.py` - Added reminder_minutes, reminder_minutes_list fields and effective_reminders property to Event
- `app/events/schemas.py` - Added reminder fields to EventCreate/EventUpdate/EventResponse with validation
- `app/events/repository.py` - Updated _to_event and create to handle reminder fields
- `app/sync/service.py` - Rewrote _event_body to use effective_reminders for Google overrides array
- `tests/test_sync_api.py` - 4 new reminder tests, 2 updated visibility tests (SimpleNamespace → Event)

## Decisions Made
- **Backward-compat dual-field:** Kept `reminder_minutes` for existing events, added `reminder_minutes_list` for multi-reminder. The `effective_reminders` property unifies access with fallback chain.
- **No config fallback in payload:** When no reminders set, `useDefault=True` delegates to Google Calendar's own default notification settings instead of using `GOOGLE_EVENT_REMINDER_MINUTES` config. This is cleaner and respects user's Google Calendar preferences.
- **Event dataclass in tests:** Replaced SimpleNamespace with Event dataclass in all `_event_body` tests since the property accessor requires the real dataclass.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated visibility tests to use Event dataclass**
- **Found during:** Task 4 (tests)
- **Issue:** Existing visibility tests used SimpleNamespace which lacks `effective_reminders` property, causing AttributeError
- **Fix:** Converted `test_event_body_includes_visibility_metadata` and `test_event_body_defaults_visibility_to_shared` to use Event dataclass
- **Files modified:** tests/test_sync_api.py
- **Committed in:** 7374563

---

**Total deviations:** 1 auto-fixed (Rule 1 - bug)
**Impact on plan:** Necessary for correctness. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Reminder model and sync payload ready for Wave 3 (integration tests)
- EventCreate/EventUpdate schemas accept reminder input; UI form can pass these fields when reminder UI is built
- All 139 tests pass (no regressions)

---
*Phase: 11-fast-day-click-manual-event-entry-with-title-start-time-end-defaults-to-1h-and-google-calendar-reminder-payload-defaults-overrides-with-ui-and-sync-test-coverage*
*Completed: 2026-03-20*
