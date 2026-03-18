# Requirements: CalendarPlanner

**Defined:** 2026-03-18
**Core Value:** A shared calendar both partners can edit that stays in sync with Google Calendar, so the family schedule is always current everywhere — on the web and on their phones.

## v1 Requirements

### Authentication & Users

- [ ] **AUTH-01**: User can sign in with their Google account via OAuth2
- [ ] **AUTH-02**: Two users can be linked to a single shared calendar household
- [ ] **AUTH-03**: User session persists across browser refresh

### Event Management

- [ ] **EVT-01**: User can create a one-time event with title, date, time, and optional description
- [ ] **EVT-02**: User can create a recurring event (daily, weekly, monthly, yearly)
- [ ] **EVT-03**: User can edit an event (title, date, time, description)
- [ ] **EVT-04**: User can delete an event
- [ ] **EVT-05**: User can view a list of upcoming events for the current day
- [ ] **EVT-06**: User can view a list of upcoming events for the current month
- [ ] **EVT-07**: Both users see events created by either user in the shared calendar

### Calendar Views

- [ ] **VIEW-01**: User can view events in a monthly calendar grid
- [ ] **VIEW-02**: User can navigate between months
- [ ] **VIEW-03**: Events show basic info (title, time) in the calendar grid

### Google Calendar Sync

- [ ] **SYNC-01**: User can export all events for a given month to their Google Calendar
- [ ] **SYNC-02**: Newly created events are automatically pushed to the linked Google Calendar
- [ ] **SYNC-03**: Event deletions are reflected in Google Calendar
- [ ] **SYNC-04**: Both users' Google Calendars receive synced events

### Natural Language Input

- [ ] **NLP-01**: User can type a natural language event description (e.g., "dentist Thursday 2pm") and the app parses it into a structured event for review
- [ ] **NLP-02**: Parsed event is shown for confirmation before saving
- [ ] **NLP-03**: User can correct any parsed fields before saving

### Image / OCR Event Extraction

- [ ] **OCR-01**: User can upload an image (e.g., event flyer, screenshot) and the app extracts date, time, and event name
- [ ] **OCR-02**: Extracted event data is shown for human review with a confidence indicator before saving
- [ ] **OCR-03**: User can edit extracted fields before saving to calendar

## v2 Requirements

### Real-Time Collaboration

- **RT-01**: Changes made by one user appear in the other user's view within seconds (SSE or WebSocket push)
- **RT-02**: Conflict detection when both users edit the same event simultaneously

### Scheduling & Reminders

- **REM-01**: User receives browser notifications for upcoming events
- **REM-02**: User can set a custom reminder time per event

### Calendar Views (Extended)

- **VIEW-04**: Weekly view
- **VIEW-05**: Agenda / list view spanning multiple weeks

### Advanced Recurrence

- **RRULE-01**: User can edit a single occurrence of a recurring event without affecting others
- **RRULE-02**: User can end a recurring event series at a specific date

### Export

- **EXP-01**: User can export calendar to .ics file for import into any calendar app

## Out of Scope

| Feature | Reason |
|---------|--------|
| More than two users / family group calendars | Household pair is the scoped use case for v1; multi-user adds significant ACL complexity |
| Native mobile app | Google Calendar on phone handles mobile via sync |
| Full two-way Google Calendar sync (v1) | Two-way sync requires conflict resolution strategy; push-only covers the core need and ships faster |
| Outlook / Apple Calendar integration | Out of scope v1; Google Calendar is the stated requirement |
| AI-generated event suggestions | Nice idea but not in stated requirements |
| Shopping lists, tasks, to-dos | Focus on events only; avoids Cozi-style feature bloat |

## Traceability

Which phases cover which requirements.

| Requirement | Phase | Goal | Status |
|-------------|-------|------|--------|
| AUTH-01 | Phase 1 | Foundation (OAuth2, auth, two-user model) | Pending |
| AUTH-02 | Phase 1 | Foundation (OAuth2, auth, two-user model) | Pending |
| AUTH-03 | Phase 1 | Foundation (OAuth2, auth, two-user model) | Pending |
| EVT-07 | Phase 1 | Foundation (OAuth2, auth, two-user model) | Pending |
| EVT-01 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| EVT-03 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| EVT-04 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| EVT-05 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| EVT-06 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| VIEW-01 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| VIEW-02 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| VIEW-03 | Phase 2 | Core Event Management (CRUD, calendar views) | Pending |
| EVT-02 | Phase 3 | Recurring Events (RRULE, RFC5545, DST) | Pending |
| SYNC-01 | Phase 4 | Google Calendar Sync (push, token management) | Pending |
| SYNC-02 | Phase 4 | Google Calendar Sync (push, token management) | Pending |
| SYNC-03 | Phase 4 | Google Calendar Sync (push, token management) | Pending |
| SYNC-04 | Phase 4 | Google Calendar Sync (push, token management) | Pending |
| NLP-01 | Phase 5 | Natural Language Input (dateparser) | Pending |
| NLP-02 | Phase 5 | Natural Language Input (dateparser) | Pending |
| NLP-03 | Phase 5 | Natural Language Input (dateparser) | Pending |
| OCR-01 | Phase 6 | Image / OCR Event Extraction (EasyOCR) | Pending |
| OCR-02 | Phase 6 | Image / OCR Event Extraction (EasyOCR) | Pending |
| OCR-03 | Phase 6 | Image / OCR Event Extraction (EasyOCR) | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23 ✓
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 after initialization*
