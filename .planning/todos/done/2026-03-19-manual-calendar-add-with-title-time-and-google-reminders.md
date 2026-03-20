---
created: 2026-03-19T16:25:42.680Z
title: Manual calendar add with title-time and Google reminders
area: ui
files:
  - app/templates/calendar.html
  - app/templates/partials/event_entry_modal.html
  - app/sync/routes.py
  - app/sync/service.py
  - tests/test_calendar_views.py
  - tests/test_sync_api.py
---

## Problem

Current calendar entry flow should support a faster day-click add path where user can choose only time and title as done criteria. Also, when events are synced to Google Calendar, reminders are not explicitly guaranteed from this app's event payload so notifications may not fire as expected.

## Solution

- Add/update day-click add-event behavior so selecting a calendar day opens manual entry prefilled for that date, requiring only title + time input to save quickly.
- Ensure synced Google events include reminder settings in Google payload (default reminders or explicit overrides) so newly created events from this app trigger Google notifications when reminder is set.
- Cover both flows with integration tests:
  - Calendar UI test for day-click prefill + minimal title/time add flow.
  - Sync API/service tests asserting reminder configuration is present for created Google events.
