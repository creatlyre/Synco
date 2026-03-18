# Research Summary: CalendarPlanner

## Executive Summary

CalendarPlanner is a **two-user household calendar web application** that solves the specific problem of keeping a couple synchronized on family events. The recommended approach uses **FastAPI + SQLite + Jinja2 + HTMX** for a lightweight, server-rendered application that syncs bidirectionally with Google Calendar, eliminating the need for a mobile app (Google Calendar handles mobile access) and JavaScript framework complexity.

The research identifies three layers of value: **(1) table stakes** (event CRUD, sharing, calendar views, Google sync), **(2) household-specific features** (user attribution, color coding, conflict detection), and **(3) differentiators** (natural language event creation, image OCR extraction). By deferring multi-user, multi-calendar, and advanced permission models, the v1 scope stays focused on households and delivers 80% of the value in 20% of the complexity.

The primary risks are **refresh token exhaustion** (Google limits 100 tokens per user per client), **timezone/DST pitfalls in recurring events**, and **concurrent edit conflicts** between the two users. These are preventable with explicit architecture patterns (token reuse, UTC-internal storage, optimistic locking).

---

## Recommended Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| **Framework** | FastAPI | 0.135.1 | Async-first, fastest Python framework (vs. Django/Flask), native OpenAPI docs, excellent for WebSocket/SSE real-time updates |
| **Server** | Uvicorn | Latest | Battle-tested ASGI server, efficient for async operations |
| **Database** | SQLite | 3.51.3 | Perfect for 2-user household scope; file-based, zero ops, ACID-compliant, upgrade path to PostgreSQL exists |
| **ORM** | SQLAlchemy | 2.x | FastAPI-native, strong typing, migration support via Alembic |
| **Frontend** | Jinja2 + HTMX | Latest | Server-rendered HTML templates + lightweight JavaScript for forms/updates; eliminates SPA complexity, instant first render |
| **Styling** | Tailwind CSS | 3.x | Utility-first, responsive, lean output |
| **Google Integration** | google-api-python-client | 2.193.0 | Official Google client, OAuth2 + Calendar API v3, full event CRUD |
| **NLP (Dates)** | dateparser | 1.3.0 | Robust relative date parsing ("next Friday," "in 3 weeks"), timezone-aware |
| **NLP (Entities)** | spaCy | 3.7 | Optional; named entity recognition for "Sarah's soccer" → participant extraction |
| **Image OCR** | EasyOCR | 1.7.2 | Offline (privacy), supports 80+ languages, asyncio-friendly |
| **Real-Time** | Polling 5-10s (Phase 1) → SSE (Phase 2) | — | Polling is simple and sufficient for household; upgrade to Server-Sent Events when needed |

**Why NOT alternatives:**
- Django: Over-engineered, slower dev cycle, unnecessary ORM overhead
- Flask: Not async-first, WebSocket support requires add-ons
- PostgreSQL (v1): Overkill for 2-user scope; SQLite adequate, migration path exists
- Cloud Vision API: Privacy concern (household data → cloud), latency, cost
- React/Vue SPA: Adds build step, bundle bloat; server-rendered sufficient

---

## Table Stakes Features

### Event Management
- **Create events** — Core functionality; one-time and recurring
- **Edit events** — Schedule changes, note updates
- **Delete events** — Remove cancelled/moved events
- **Event fields** — Title, start/end time, description, recurring pattern (RRULE)
- **Recurring patterns** — Weekly, monthly, yearly with frequency control
- **User attribution** — "Sarah added dentist appointment" visibility

### Sharing & Collaboration
- **Two-user shared calendar** — Both household members can view and edit the same calendar
- **Google Calendar export** — Push events to Google Calendar (phone access, reminders)
- **Real-time sync** — Changes visible to other user within 5-10 seconds
- **Conflict detection** — Alert when both users have overlapping events

### Calendar Views
- **Month view** — Full month overview with event indicators
- **Week view** — Multi-day layout with time grid
- **Day view** — Detailed view of single day
- **Upcoming events list** — Next N days without switching views
- **Today indicator** — Always know current date

### Mobile Access & Notifications
- **Mobile-responsive design** — Works on phone browser (no native app)
- **In-app notifications** — Alert when event added/modified
- **Reminder selection** — "Alert 15 min before," "1 day before," "on day"
- **Google Calendar notifications** — Leverage Google's notification system on phone

---

## Differentiating Features

| Feature | Why Valuable | Complexity |
|---------|-------------|-----------|
| **Natural language event creation** | "Mom's dentist appointment Tuesday 2pm" → auto-creates event (10x faster than form fill) | High |
| **Image/document OCR** | Photograph flyer/invitation → extract date/time/name automatically | High |
| **Color coding by person** | Visual identification: Sarah=red, Tom=blue | Low |
| **Quick add templates** | "Sarah practice," "Doctor appointment" with pre-set details | Low |
| **Event search** | Find "dentist" across all events | Low |
| **Conflict highlighting** | Visual alert when both users scheduled simultaneously | Medium |
| **PDF export** | Print calendar for fridge | Low |
| **iCal/ICS export** | Portable calendar format | Low |

---

## Architecture Overview

CalendarPlanner follows a **three-tier service-oriented architecture**:

```
Web Frontend (Jinja2 templates, HTMX forms)
    ↓ REST API
Service Layer (Event, Recurrence, GoogleSync, NLP, OCR services)
    ↓ Repository Pattern
Data Access (SQLAlchemy ORM)
    ↓
SQLite Database

External: Google Calendar API (OAuth2, Event CRUD)
```

**Key components:**
1. **EventService** — CRUD operations, validation, recurrence expansion
2. **RecurrenceService** — RFC5545 RRULE parsing and instance generation (handles DST/timezone)
3. **GoogleSyncService** — OAuth2 flow, token management, push/pull events
4. **CalendarService** — Two-user shared calendar model, access control
5. **NLPService** — Natural language → event fields (uses dateparser + spaCy)
6. **OCRService** — Image extraction → text → event fields (uses EasyOCR)

**Build order by dependency:**
1. Database schema (events, users, sync state)
2. EventService + Recurrence (core calendar logic)
3. CalendarService + auth (two-user sharing model)
4. REST API endpoints (CRUD, views)
5. GoogleSyncService (OAuth + sync)
6. Frontend (Jinja2 templates + HTMX)
7. NLPService (natural language input)
8. OCRService (image extraction)

---

## Top Pitfalls to Avoid

### 1. Refresh Token Exhaustion
**Prevention:** Store one refresh token per user permanently in encrypted DB field; reuse it for all API calls. Use "Production" consent screen (not "Testing") from day one. Implement graceful token failure handling (flag user for re-auth but don't crash). Monitor `invalid_grant` errors in logs.

### 2. Recurring Events + Timezone/DST Disasters
**Prevention:** Always store times in UTC internally; render to users in local timezone only at UI layer. Use mature RRULE library (`dateutil`), never implement recurrence yourself. Hard-test DST boundaries (Nov 5, Mar 9). In v1, disallow editing single recurring instances; treat as separate events. Fetch full series from Google on each sync.

### 3. Concurrent Edit Conflicts & Lost Updates
**Prevention:** Implement optimistic locking—store `last_edited_at` and `last_editor_user_id` with each event. When saving, check if event changed; if yes, show conflict dialog. Queue-based sync: lock event during editing (UI shows "B is editing this"). Log all conflicts for later conflict-resolution feature.

### 4. OCR Accuracy & Fallback Failure
**Prevention:** **Never auto-add OCR results**; always require human review. Show OCR confidence per field; highlight low-confidence (< 75%) in yellow. Display raw image + text input form if OCR fails entirely. Validate before sync: date in future, title not empty, location not garbage. Async background processing with user notification.

### 5. NLP Date Parsing Edge Cases
**Prevention:** In v1, limit NLP to explicit formats ("March 15, 2026") or dropdowns ("in X days"). If using relative dates, validate against user's timezone + current date. Validate future dates; if ambiguous (e.g., "March 15" in December), ask user: "Did you mean 2026 or 2027?". Pass user's timezone to NLP parser explicitly.

---

## Phase Recommendations

Based on feature dependencies and risk mitigation:

### Phase 1: Foundation (Database, Auth, Event CRUD)
Create core schema (events, users, recurring rules). Implement user authentication (OAuth2 with Google). Build EventService for create/edit/delete. Add basic Jinja2 templates for event list. Deploy to test instance. **Duration: 2-3 weeks**

### Phase 2: Calendar Views & Sharing
Implement month/week/day views. Add CalendarService for two-user sharing model. Build calendar grid UI. Add in-app notifications (polling at 5-10s intervals). Test multi-user editing workflow. **Duration: 2-3 weeks**

### Phase 3: Recurring Events (With RFC5545 Support)
Implement RecurrenceService using `dateutil.rrule`. Add UI for frequency/end date selection. Hard-test DST boundaries (Mar/Nov). Support EXDATE (skip instances). **Duration: 2-3 weeks**

### Phase 4: Google Calendar Sync (Push-Only)
Implement GoogleSyncService with OAuth2 refresh token handling. Add "Export to Google" button. Build sync state tracking. Monitor token health. Test two-user push workflow. **Duration: 2-3 weeks**

### Phase 5: Real-Time Sync Optimization (Polling → SSE)
Replace 5-10s polling with Server-Sent Events (one-way push). Add user attribution ("Sarah added event"). Build conflict detection UI. **Duration: 1-2 weeks**

### Phase 6: Natural Language Event Creation
Integrate `dateparser` for relative date parsing ("next Friday," "in 3 days"). Add NLP input box to UI. Validate parsed dates (future, valid time range). Fallback to form if parsing uncertain. **Duration: 2-3 weeks**

### Phase 7: Image OCR for Event Extraction
Integrate EasyOCR. Build image upload form. Extract text → parse with dateparser. **Human review step required** (never auto-add). Show OCR confidence per field. **Duration: 2-3 weeks**

### Phase 8: Polish & Monitoring
Add conflict resolution UI ("Edit yours" / "Use theirs"). Implement event search. Add color coding by person. Build email digests (optional). Add monitoring/alerting for token health, sync failures. Polish mobile UX. **Duration: 1-2 weeks**

---

## Research Confidence Assessment

| Area | Confidence | Basis |
|------|------------|-------|
| **Stack** | HIGH | Official docs (FastAPI, SQLAlchemy), TechEmpower benchmarks, Google API client maturity |
| **Features** | HIGH | Domain research (Cozi, Google Calendar, Apple Family Sharing), household calendar patterns well-established |
| **Architecture** | HIGH | RFC5545 (RRULE standard), OAuth2 (Google docs), three-tier pattern is proven |
| **Pitfalls** | MEDIUM-HIGH | Mix of official Google warnings (refresh tokens), known RRULE edge cases (timezone/DST), and common patterns |

**Gaps identified:**
- **Specific NLP accuracy rates:** Research didn't test exact dateparser edge cases; Phase 6 should include test suite
- **Refresh token behavior:** Google docs vague on exact rotation limits; implement monitoring early to detect issues
- **OCR accuracy on household materials:** Research generic; Phase 7 should test on actual flyers/invitations
- **Concurrent edit performance:** Research covered patterns but not benchmarks; Phase 4 should load-test

---

## Sources

- **STACK.md:** Official docs (FastAPI, SQLAlchemy, google-api-python-client), TechEmpower benchmarks, 2026 Python ecosystem survey
- **FEATURES.md:** Cozi documentation, Google Calendar, Apple Family Sharing, household calendar market analysis
- **ARCHITECTURE.md:** RFC5545 standard (RRULE), OAuth2 spec, three-tier architecture patterns, Google Calendar API reference
- **PITFALLS.md:** Google OAuth2 limits, dateutil RRULE edge cases, household calendar UX patterns, concurrent edit consensus patterns

---

## Ready for Planning

Research complete. **Roadmap can now proceed with 5-8 phases** structured by dependency:
1. **Foundation** (auth + event CRUD)
2. **Views + Sharing** (multi-user calendar)
3. **Recurrence** (RRULE support)
4. **Google Sync** (OAuth2 + push)
5. **Real-time** (polling → SSE)
6. **NLP** (natural language input)
7. **OCR** (image extraction)
8. **Polish** (monitoring, UX)

Highest-risk items flagged for early attention: token exhaustion prevention (Phase 4), timezone edge cases (Phase 3), conflict handling (Phase 5).
