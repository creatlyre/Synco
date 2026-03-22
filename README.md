# Synco

Shared household calendar & budget planner for two users with Google sign-in, shared events, recurrence, Google Calendar sync, natural-language quick add, and OCR-assisted event extraction.

## Why This Project

Synco is designed for a couple/household that wants one shared source of scheduling truth while still receiving reminders on phones through Google Calendar.

## Current Status

- Version: v1.0.0
- Milestone: v1.0 shipped (tag: `v1.0`)
- Core scope complete:
  - Google OAuth sign-in and session handling
  - Two-user household invite and shared calendar model
  - Event CRUD + month/day calendar views
  - RFC5545 recurrence support
  - Google Calendar export and sync hooks
  - Natural-language event parsing
  - OCR image parsing with review/fallback
  - Modal-first UI/UX and mobile improvements

## Feature Highlights

- Household sharing
  - Invite flow to link two users to one shared calendar.
- Event management
  - Create, edit, delete events.
  - Daily and monthly views.
- Recurrence
  - Daily, weekly, monthly, yearly recurrence via RRULE patterns.
- Google integration
  - Export month to Google Calendar.
  - Sync on create/update/delete hooks.
- Quick add (NLP)
  - Parse input like "dentist Thursday 2pm" into structured event data.
  - Ambiguity handling for year selection when dates are unclear.
- OCR quick add
  - Upload image, extract text, parse event fields.
  - Confidence-based review and manual fallback.
- UX polish
  - Manual entry modal, quick-add bridge, keyboard behavior, mobile layout.

## Tech Stack

- Backend: FastAPI
- Templating/UI: Jinja2 + server-rendered HTML
- Data store: Supabase (Postgres-backed API layer)
- Auth: Google OAuth2 (plus Supabase auth session support)
- Sync: Google Calendar API
- Parsing: dateparser/dateutil-style NLP + optional EasyOCR
- Tests: pytest

## Repository Layout

```text
app/
  auth/          # OAuth/session/auth routes and utilities
  database/      # Supabase store/data access abstractions
  events/        # Event APIs, NLP, OCR, recurrence, service layer
  middleware/    # Session validation middleware
  sync/          # Google sync APIs and service
  users/         # Household/invitation APIs and service
  views/         # Calendar page routes
  templates/     # Jinja templates and modal partials

tests/           # API, integration, NLP, recurrence, sync, and view tests
main.py          # FastAPI app entry point
config.py        # Environment-driven settings
```

## Prerequisites

- Python 3.10+
- pip / virtualenv
- Supabase project (URL + keys)
- Google Cloud OAuth credentials (client ID/secret)

Optional for full OCR behavior:
- `easyocr` package and runtime dependencies

## Quick Start

1. Clone and enter the repo.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure environment variables.
5. Run the app.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
- App: `http://localhost:8000`
- Health: `http://localhost:8000/health`

## Environment Variables

Create a `.env` file in the project root.

Required for normal operation:

```env
DEBUG=true
SECRET_KEY=replace-with-strong-secret
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=8

SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>

GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
GOOGLE_EVENT_REMINDER_MINUTES=30

DB_ENCRYPTION_KEY=replace-with-strong-encryption-key
```

Notes:
- `config.py` also supports fallback names like `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- OCR endpoint returns graceful errors when EasyOCR is not installed.

## API Overview

Auth:
- `GET /auth/login`
- `GET /auth/callback`
- `POST /auth/session`

Users/household:
- `GET /api/users/me`
- `GET /api/users/household`
- `POST /api/users/invite`
- `POST /api/users/accept-invitation`

Events:
- `POST /api/events`
- `PUT /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `GET /api/events/day`
- `GET /api/events/month`
- `POST /api/events/parse`
- `POST /api/events/ocr-parse`

Sync:
- `POST /api/sync/export-month`
- `POST /api/sync/import-month`
- `GET /api/sync/status`

## Testing

Run all tests:

```bash
pytest -q
```

Run common targeted suites:

```bash
pytest -q tests/test_auth.py tests/test_users.py
pytest -q tests/test_calendar_views.py tests/test_events_api.py tests/test_sync_api.py
pytest -q tests/test_nlp.py tests/test_recurrence.py
```

## Release and Milestones

- Current release tag: `v1.0`
- Milestone archive: `.planning/milestones/`
- Planning system: GSD workflows under `.planning/`

Useful workflow commands:
- `/gsd-new-milestone` to start next milestone planning.
- `/gsd-progress` to inspect current execution/planning state.

## Security Notes

- Do not commit real secrets.
- Rotate `SECRET_KEY` and `DB_ENCRYPTION_KEY` for production.
- Use secure cookie settings and HTTPS in production environments.

## License

No license file is currently included. Add one before public distribution if needed.
