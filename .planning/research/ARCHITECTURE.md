# Architecture Patterns

**Domain:** Shared household calendar with Google Calendar integration
**Researched:** March 18, 2026
**Confidence:** HIGH

## System Architecture Overview

The CalendarPlanner follows a **three-tier layered architecture** with event sync coordination:

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB FRONTEND                               │
│  (Flask/FastAPI templates, Vue/React for reactive UI)            │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                     API LAYER (REST)                              │
│  ├─ Event endpoints (CRUD)                                        │
│  ├─ Calendar endpoints                                            │
│  ├─ Google sync endpoints                                         │
│  ├─ NLP processing endpoint                                       │
│  └─ OCR upload endpoint                                           │
└────────────┬─────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                  │
│  ├─ EventService (create, update, delete, query)                │
│  ├─ CalendarService (shared calendar mgmt)                       │
│  ├─ RecurrenceService (RRULE processing)                         │
│  ├─ GoogleSyncService (OAuth2, API integration)                 │
│  ├─ NLPService (text parsing, intent extraction)                 │
│  └─ OCRService (image processing, text extraction)              │
└────────────┬─────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                              │
│  ├─ EventRepository (persistence)                               │
│  ├─ UserRepository                                               │
│  ├─ CalendarRepository                                           │
│  └─ GoogleSyncStateRepository (sync metadata)                   │
└────────────┬─────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                        DATABASE                                   │
│  (SQLite for v1, PostgreSQL recommended for production)          │
└─────────────────────────────────────────────────────────────────┘

         External Integration
┌──────────────────────────────┐
│   Google Calendar API (v3)   │
│  ├─ OAuth2 authentication   │
│  ├─ Event push/pull          │
│  └─ Access control list (ACL)│
└──────────────────────────────┘
```

## Component Boundaries

### 1. **Web Frontend** (User Interface)
- **Responsibility:** Display calendar view, month/day views, event creation UI
- **Communicates with:** REST API Layer only
- **Technology:** HTML/CSS/JavaScript (Vue.js or vanilla JS recommended for simplicity)
- **Key features:**
  - Calendar month view with events
  - Event creation/editing modal
  - NLP input box for natural language events (e.g., "Dinner Friday 7pm")
  - Image upload area for OCR events
  - User authentication (two-user model)
  - Settings/sync status indicator

### 2. **REST API Layer**
- **Responsibility:** Route HTTP requests to services, validate input, return JSON responses
- **Technology:** Flask or FastAPI (FastAPI recommended for async tasks)
- **Endpoints:**
  ```
  GET    /api/events              # List events for date range
  POST   /api/events              # Create event
  GET    /api/events/{id}         # Get event details
  PUT    /api/events/{id}         # Update event
  DELETE /api/events/{id}         # Delete event (soft delete recommended)
  
  POST   /api/events/nlp          # Create event from natural language
  POST   /api/events/ocr          # Create event from image upload
  
  GET    /api/calendar            # Get shared calendar metadata
  POST   /api/calendar/sync       # Trigger sync with Google Calendar
  GET    /api/calendar/sync-status # Check last sync status
  
  GET    /api/auth/login         # OAuth2 callback redirect
  POST   /api/auth/logout        # Sign out
  ```

### 3. **EventService** (Core event logic)
- **Responsibility:** Event CRUD operations, validation, recurrence expansion
- **Communicates with:** EventRepository, RecurrenceService, CalendarService
- **Key methods:**
  ```python
  create_event(title, start, end, rrule=None, user_id)
  update_event(event_id, changes)
  delete_event(event_id, cascade_to_google=True)
  get_events_for_range(start_date, end_date)
  get_recurrence_instances(event_id, start, end)
  create_exception(event_id, instance_date, new_start, new_end)
  ```
- **Validation:** Ensures DTSTART < DTEND, time zones handled correctly, RRULE is valid

### 4. **RecurrenceService** (RFC5545 RRULE processor)
- **Responsibility:** Parse, validate, and expand RRULE patterns
- **Communicates with:** Database (reads RRULE strings)
- **Algorithms needed:**
  - Parse RRULE string into structured format: `FREQ=daily;COUNT=10;INTERVAL=2`
  - Generate recurrence instances: Given DTSTART + RRULE, compute all occurrences within a date range
  - Handle EXDATE (exceptions): Remove specific instances from recurrence set
  - Handle RDATE (recurrence dates): Add manual override dates
  - Handle time zones in recurrence (DST transitions can affect times)
  - Modify "this and future" instances (RANGE=THISANDFUTURE parameter)
- **Implementation approach:**
  - Use `dateutil.rrule` library (Python, RFC5545 compliant) OR
  - Implement custom parser if simpler control needed
- **Key RFC5545 concepts:**
  - DTSTART: Event start time (serves as anchor for RRULE)
  - RRULE: Defines repetition pattern
  - EXDATE: Dates to exclude (e.g., skip a holiday)
  - RDATE: Manual dates to include (e.g., add makeup meeting)
  - RECURRENCE-ID: Identifies specific instance in recurrence set (for exceptions)

### 5. **GoogleSyncService** (Google Calendar API integration)
- **Responsibility:** OAuth2 auth, bi-directional sync with Google Calendar
- **Communicates with:** EventService, GoogleSyncStateRepository, external Google API
- **Tech stack:** `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`
- **Key operations:**
  ```python
  authorize_user(user_id)                     # OAuth2 login flow
  push_event_to_google(event_id)              # Create/update event on Google
  pull_events_from_google(user_id, date_range) # Fetch Google events (one-way for v1)
  delete_event_from_google(event_id)         # Remove from Google Calendar
  sync_all_events(user_id, month)            # Batch sync for a month
  ```
- **Sync strategy (v1 - Push only):**
  - App is source of truth (shared calendar)
  - All changes push → Google Calendar via API
  - Google Calendar acts as notification/mobile access tier
  - No conflict resolution needed (no pull overwrites)
  - Store last sync timestamp to detect if app and Google drift
- **OAuth2 flow:**
  1. User clicks "Connect Google Calendar"
  2. Redirected to Google auth consent screen
  3. Google returns auth code
  4. Exchange code for access token + refresh token
  5. Store refresh token in secure DB (for long-lived access)
  6. Use access token for API calls, refresh when expired

### 6. **CalendarService** (Shared calendar management)
- **Responsibility:** Manage two-user sharing model, access control
- **Communicates with:** CalendarRepository, GoogleSyncService
- **Key concepts:**
  - One calendar per household pair (2 users)
  - Calendar is bound to User 1's Google Calendar (single source of truth externally)
  - User 2 accesses via shared link or app login (internal auth only)
  - Both users can create/edit events in shared calendar
  - Both users sync to same Google Calendar (User 1's)
- **Key methods:**
  ```python
  create_shared_calendar(user1_id, user2_id)
  add_user_to_calendar(user_id, calendar_id)
  remove_user_from_calendar(user_id, calendar_id)
  get_users_for_calendar(calendar_id)
  get_calendar_color_preferences(user_id)
  ```

### 7. **NLPService** (Natural Language Event Creation)
- **Responsibility:** Parse natural language input into event components
- **Communicates with:** EventService
- **Tech stack:** `spacy` or `textblob` (lightweight) for NER, or `openai` API (GPT-3.5) for smarter parsing
- **Input → Output transformation:**
  ```
  "Dinner Friday 7pm" → {title: "Dinner", date: <next Friday>, time: "19:00"}
  "Team meeting Tuesday 2-3pm" → {title: "Team meeting", date: <Tuesday>, start: "14:00", end: "15:00"}
  "Every Monday 9am sync" → {title: "sync", rrule: "FREQ=weekly;BYDAY=MO", time: "09:00"}
  ```
- **Fallback strategy:** If parsing uncertain, return partial event + ask user to confirm
- **Placement in flow:**
  - Run on client or server? (Server recommended for security & consistency)
  - Async processing? (Yes, if using AI API to avoid delays)

### 8. **OCRService** (Image-based event extraction)
- **Responsibility:** Extract event info from images (flyers, screenshots)
- **Communicates with:** EventService
- **Tech stack:** `pytesseract` (Tesseract OCR) or `paddleocr` for text extraction; `OpenAI Vision API` for semantic understanding
- **Pipeline:**
  1. User uploads image
  2. OCR extracts text
  3. NLP parses extracted text for dates, times, event names
  4. Create event from parsed data (with user confirmation)
- **Use cases:**
  - Extract date/location from physical flyer
  - Screenshot of email with event details
  - Photo of whiteboard with meeting schedule

---

## Data Model

### Core Entities

#### **Event**
Represents a calendar event (single or recurring instance).

```python
class Event:
    id: UUID                  # Unique identifier
    calendar_id: UUID         # Which calendar
    created_by: UUID          # User who created
    title: str                # Event name
    description: Optional[str]
    
    # Time info
    dtstart: datetime         # Start time (with timezone)
    dtend: datetime           # End time (with timezone)  
    all_day: bool             # All-day event flag
    
    # Recurrence
    rrule: Optional[str]      # RFC5545 RRULE (e.g., "FREQ=WEEKLY;BYDAY=MO")
    exdate: Optional[list]    # Excluded dates for exceptions
    rdate: Optional[list]     # Extra dates to include
    recurrence_id: Optional[datetime]  # Identifies instance in recurrence set
    
    # Metadata
    location: Optional[str]
    color: Optional[str]      # Display color
    status: str               # "CONFIRMED", "TENTATIVE", "CANCELLED"
    transparency: str         # "OPAQUE" (busy) or "TRANSPARENT" (free)
    
    # Sync state
    google_event_id: Optional[str]    # Google Calendar event ID
    last_synced_at: Optional[datetime]
    pending_google_sync: bool
    
    # Change tracking
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]    # Soft delete
```

#### **User**
Represents a household member.

```python
class User:
    id: UUID
    username: str
    email: str
    password_hash: str        # Hashed password
    
    # Google integration
    google_oauth_token: Optional[str]        # Access token
    google_oauth_refresh_token: Optional[str] # Refresh token
    google_calendar_id: Optional[str]         # Their Google Calendar ID
    google_auth_expires_at: Optional[datetime]
    
    # Preferences
    timezone: str             # "America/New_York", etc.
    created_at: datetime
```

#### **Calendar**
Represents a shared calendar (household).

```python
class Calendar:
    id: UUID
    name: str                 # e.g., "Household"
    description: Optional[str]
    
    # Users in this calendar
    user_ids: list[UUID]      # Always exactly 2 for v1
    
    # Google sync target
    primary_user_id: UUID     # Whose Google Calendar we sync to
    google_calendar_id: Optional[str]
    
    # Metadata
    created_at: datetime
    color: str                # Display color
    
    # Sync tracking
    last_full_sync_at: Optional[datetime]
    next_sync_at: Optional[datetime]
```

#### **GoogleSyncState** (Metadata for sync coordination)
```python
class GoogleSyncState:
    id: UUID
    calendar_id: UUID
    user_id: UUID
    
    # Sync metadata
    last_sync_token: Optional[str]      # Google's sync token for incremental sync
    last_synced_at: datetime
    pending_events: list[UUID]          # Events waiting to push
    pending_deletes: list[str]          # Google event IDs to delete
    
    # Error tracking
    last_sync_error: Optional[str]
    sync_error_count: int
    retry_after: Optional[datetime]
```

#### **EventException** (For handling "this and future" edits)
```python
class EventException:
    id: UUID
    parent_event_id: UUID     # Reference to base recurring event
    recurrence_id: datetime   # Which instance this modifies
    
    # Modified fields
    title: Optional[str]
    dtstart: Optional[datetime]
    dtend: Optional[datetime]
    location: Optional[str]
    
    # Indicates range of effect
    range: str                # "THISONLY" or "THISANDFUTURE"
    
    created_at: datetime
```

---

## Data Flow

### 1. **Create Event (UI → App → Google)**
```
User enters event details (title, date, time)
           ↓
Browser POST /api/events {title, dtstart, dtend}
           ↓
API validates input
           ↓
EventService.create_event() → Database INSERT
           ↓
Event created with status="pending_sync"
           ↓
GoogleSyncService.push_event_to_google(event_id)
           ↓
API calls Google Calendar API:
  - POST /calendar/v3/calendars/{calendarId}/events
  - Body: iCalendar format with DTSTART, DTEND, RRULE (if recurring)
           ↓
Google returns event_id
           ↓
Store google_event_id in database, mark synced
           ↓
Return event to UI with confirmation
```

### 2. **Create Recurring Event (Adding an RRULE)**
```
UI: User selects "repeat weekly"
           ↓
EventService.create_event(rrule="FREQ=WEEKLY;BYDAY=MO,WE,FR")
           ↓
RecurrenceService validates:
  - FREQ is present ✓
  - BYDAY format valid ✓
  - No conflicting COUNT + UNTIL ✓
           ↓
Store event with rrule string
           ↓
GoogleSyncService pushes to Google with RRULE property:
  SUMMARY:Meeting
  DTSTART:20260401T090000Z
  RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR
           ↓
Google interprets and creates recurrence set
```

### 3. **Edit Exception (This and Future)**
```
User clicks "Edit this and future" on July 15 meeting
           ↓
UI sends: PUT /api/events/{id} with RANGE=THISANDFUTURE
  {recurrence_id: "2026-07-15T09:00", title: "Team Sync (Hybrid)", location: "Zoom"}
           ↓
EventService detects:
  - Base event has rrule
  - This is exception (recurrence_id provided)
           ↓
Create EventException record with range=THISANDFUTURE
           ↓
RecurrenceService.modify_recurrence_range():
  - Split old RRULE at July 15: UNTIL=20260715
  - Copy base event, set DTSTART=July 15, new changes
           ↓
GoogleSyncService:
  1. Modify original Google event: add UNTIL=20260714
  2. Create new Google event: starts July 15, with changes
           ↓
UI shows updated calendar with new instance series
```

### 4. **Sync with Google Calendar (Monthly Export)**
```
User clicks "Sync to Google" or auto-sync timer fires
           ↓
GoogleSyncService.sync_all_events(calendar_id, month=March2026)
           ↓
Get all events in calendar for March
           ↓
For each event:
  IF google_event_id exists:
    - Call Google PUT endpoint (update)
  ELSE:
    - Call Google POST endpoint (create)
           ↓
Handle failures:
  - Store in pending_events queue
  - Retry on next sync
           ↓
Update last_synced_at timestamp
           ↓
UI shows "Synced March 1-31" notification
```

### 5. **Create Event from NLP**
```
User types: "Dinner with Sarah Friday 7pm"
           ↓
POST /api/events/nlp {text: "Dinner with Sarah Friday 7pm"}
           ↓
NLPService.parse(text):
  - Extract title: "Dinner with Sarah"
  - Extract relative_date: "Friday" → next Friday's date
  - Extract time: "7pm" → 19:00
           ↓
EventService.create_event(
    title="Dinner with Sarah",
    dtstart=26-04-04T19:00,
    dtend=26-04-04T20:30,  # +1.5h default
    status="TENTATIVE"       # User confirms before saving
)
           ↓
Return partial event to UI for confirmation
           ↓
User clicks "Save" → full event creation pipeline
```

### 6. **Create Event from OCR**
```
User uploads image of event flyer
           ↓
POST /api/events/ocr {image_file}
           ↓
OCRService.extract_text(image):
  - Use pytesseract to OCR → "Team Annual Retreat\nJune 15-17, 2026\nLocation: Mountain Lodge"
           ↓
NLPService.parse(text):
  - title: "Team Annual Retreat"
  - start: 2026-06-15 (all-day)
  - end: 2026-06-17 (3-day event)
  - location: "Mountain Lodge"
           ↓
Return suggested event to UI
           ↓
User edits and confirms
           ↓
Create event with all_day=true, multi-day span
```

---

## Recurrence Model (RFC5545 RRULE)

### RRULE Syntax
```
RRULE:FREQ=frequency;[INTERVAL=n];[COUNT=n];[UNTIL=datetime];[BYDAY=days];[BYMONTH=months];...
```

### Common Examples
```
# Every weekday, 10 times
DTSTART:20260401T090000Z
RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR;COUNT=10

# Every other week on Tue/Thu until end of year
DTSTART:20260401T090000Z
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TU,TH;UNTIL=20261231T235959Z

# First Monday of each month, forever
DTSTART:20260401T090000Z
RRULE:FREQ=MONTHLY;BYDAY=1MO

# Last day of month, 12 times
DTSTART:20260131T090000Z
RRULE:FREQ=MONTHLY;BYMONTHDAY=-1;COUNT=12

# Every year on anniversary
DTSTART:20260620T100000Z
RRULE:FREQ=YEARLY
```

### Key Implementation Details
- **DTSTART drives the recurrence:** Time zone, day of week, time of day all derive from DTSTART if not explicitly overridden by BYDAY, BYHOUR, etc.
- **EXDATE excludes instances:** If you mark an instance as "cancelled", add its datetime to EXDATE
- **RANGE=THISANDFUTURE:** Creates two rules: old rule ends day before, new rule starts at exception date
- **Time zone handling:** DTSTART can specify TZID (e.g., DTSTART;TZID=America/New_York:...)
- **DST transitions:** Recurring events should use local time + explicit TZID to handle DST correctly

---

## Google Calendar API Integration Pattern

### OAuth2 Flow (Client-Side Authentication)
```
┌─────────────┐                                    ┌──────────────┐
│   Web App   │                                    │ Google OAuth │
└──────┬──────┘                                    └──────┬───────┘
       │                                                  │
       │ 1. Click "Login with Google"                   │
       ├─────────────────────────────────────────────► │
       │                                                │
       │ 2. Redirect to Google consent screen          │
       │ ◄────────────────────────────────────────────┤
       │                                                │
       │ 3. User approves (calendar.events scope)      │
       │                                                │
       │ 4. Authorization code redirect                │
       │ ◄────────────────────────────────────────────┤
       │                                                │
       │ 5. Exchange code for access + refresh tokens  │
       │                                                │
       │ 6. Store refresh token securely in DB        │
       │                                                │
       └─────────────────────────────────────────────────┘

Access Token: Short-lived (1 hour), used for API calls
Refresh Token: Long-lived, used to get new access tokens
```

### Event Sync with Google (Push Model - v1)

#### Create Event on Google
```http
POST /calendar/v3/calendars/{calendarId}/events
Authorization: Bearer {accessToken}

{
  "summary": "Team Meeting",
  "description": "Quarterly planning",
  "start": {
    "dateTime": "2026-04-15T14:00:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2026-04-15T15:00:00",
    "timeZone": "America/New_York"
  },
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=WE;UNTIL=20260630"]
}

Response:
{
  "id": "abc123def456ghi789",
  "etag": "...",
  ...
}
```

#### Update Event on Google
```http
PUT /calendar/v3/calendars/{calendarId}/events/{eventId}
Authorization: Bearer {accessToken}

{
  "summary": "Team Meeting (Rescheduled)",
  "start": {...},
  "end": {...}
}
```

#### Delete Event on Google
```http
DELETE /calendar/v3/calendars/{calendarId}/events/{eventId}
Authorization: Bearer {accessToken}
```

### Incremental Sync (Future Enhancement)
```python
# Use sync token for efficient updates (don't fetch all events)
events_page = service.events().list(
    calendarId='primary',
    syncToken='latest_sync_token_from_db'
).execute()

# Only returns changed events since last sync
for event in events_page.get('items', []):
    if event.get('status') == 'cancelled':
        delete_from_db(event['id'])
    else:
        upsert_to_db(event)

# Store new sync token
new_sync_token = events_page.get('nextSyncToken')
```

---

## NLP & OCR Placement in Architecture

### NLP Service Deployment
- **Location:** Server-side (not client)
- **Reasons:** 
  - Consistency (same parser for all users)
  - Security (no exposing parsing rules to client)
  - Async capability (queue NLP jobs if slow)
- **Process:**
  ```
  POST /api/events/nlp {text}
    → Queue job (if using AI API)
    → NLPService.parse()
    → Return suggested event JSON
    → User confirms
    → EventService.create_event() (same as manual)
  ```

### OCR Service Deployment
- **Location:** Server-side upload
- **Process:**
  1. User selects image file
  2. Upload to server, store temporarily
  3. OCRService.extract_text() using Tesseract/PaddleOCR
  4. NLPService.parse() on extracted text
  5. Return suggested event + image preview
  6. User confirms or edits
  7. Delete temporary image, create event

---

## Build Order (Component Dependencies)

**Phase 1: Foundation**
1. Database schema + initialization
2. User/Calendar/Event entities
3. Data access layer (repositories)

**Phase 2: Core Calendar (No sync yet)**
4. EventService (CRUD)
5. RecurrenceService (RRULE parsing/expansion)
6. CalendarService (two-user sharing)
7. REST API endpoints for events
8. Basic frontend calendar views

**Phase 3: Google Integration**
9. GoogleSyncService (OAuth2, API calls)
10. Sync state tracking
11. Push-to-Google pipeline
12. "Sync" button in UI

**Phase 4: NLP & OCR (Enhancement)**
13. NLPService
14. OCRService
15. Post-processing for confidence scores
16. UI for NLP/OCR input methods

**Phase 5: Polish**
17. Error handling, retry logic
18. Notifications
19. Testing, performance optimization

---

## Key Architectural Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **Push-only sync (v1)** | Reduces complexity; no conflict resolution needed | App is source of truth; Google is read-on-mobile mirror |
| **Single shared calendar** | Simplest model for household pair | No multi-calendar complexity, no permission matrix |
| **RFC5545 RRULE** | Standard, Google Calendar uses it | Can exchange with any RFC5545-compliant system |
| **Server-side NLP/OCR** | Consistency, security, easier to upgrade | Slightly higher latency but better UX/maintainability |
| **SQLite → PostgreSQL path** | Fast initial development → production scaleability | Use SQLAlchemy ORM for portability |
| **OAuth2 for Google** | Industry standard, secure | Users don't share passwords, long-lived refresh tokens |

---

## Integration Points with External Systems

### Google Calendar API
- **Scope:** `calendar.events`, `calendar.readonly` (for future pull-sync)
- **Rate limits:** 100 requests/second per user (safe for household use)
- **Quota:** 1 million requests/day (easily sufficient)
- **Retry strategy:** Exponential backoff on 429/500 errors

### Dependencies for NLP/OCR
- **NLP:** `spacy` (lightweight) or GPT API (smarter)
- **OCR:** `pytesseract` (Tesseract) or `paddleocr` (no external deps)
- **Async queue:** `Celery` + Redis (if background processing needed)

---

## Hidden Complexity Flags

| Area | Complexity | Mitigation |
|------|-----------|-----------|
| **Recurrence exceptions** | THISANDFUTURE splits base rule; sync requires careful merging | Document RANGE logic; test thoroughly |
| **Time zone handling** | DST transitions, floating times vs. UTC | Always use explicit TZID; handle DST edge cases in tests |
| **OAuth2 token refresh** | Refresh tokens expire; background jobs fail silently | Implement automatic refresh on 401; monitor token age |
| **Sync conflicts** | If user edits on both Google & app (despite v1 design) | Add conflict detection; prefer app (source of truth) |
| **Soft deletes** | Must respect deleted_at in all queries | Add filters to all queries; audit trail important |

---

## Recommended Build Sequence for Phases

1. **Phase 1:** Database + EventService (no recurrence yet)
2. **Phase 2:** RecurrenceService (test RRULE expansion heavily)
3. **Phase 3:** REST API + basic UI (month view)
4. **Phase 4:** GoogleSyncService + OAuth2
5. **Phase 5:** NLP (simple rule-based first, AI later)
6. **Phase 6:** OCR (add last, most fragile)
7. **Phase 7:** Exception handling + "this and future" edits

Each phase represents 1-2 weeks of development for a single developer.

## Sources

- [Google Calendar API Overview](https://developers.google.com/workspace/calendar/api/guides/overview) - Official Google docs on Event, Calendar, ACL resources
- [RFC 5545 - iCalendar Specification](https://datatracker.ietf.org/doc/html/rfc5545) - Authoritative RRULE, DTSTART, recurrence model definition
- Confidence: **HIGH** — Both sources are authoritative (Google official docs + IETF standards)
