# Technology Stack - 2026

**Project:** CalendarPlanner (Shared Household Calendar)
**Researched:** March 18, 2026
**Python Version:** 3.10+

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|-----------|---------|---------|-----|
| **FastAPI** | 0.135.1 | Web API Framework | Fastest Python async framework (per TechEmpower benchmarks), built-in OpenAPI docs, native async/await, excellent for two-user real-time sync. Significantly faster dev cycle than Flask/Django. |
| **Uvicorn** | Latest | ASGI Server | Battle-tested async server, used by FastAPI, efficient for WebSocket/real-time operations. |
| **Pydantic** | v2.x | Data Validation | FastAPI-native validation, strong typing, serialization to JSON. |

**Why NOT Django/Flask:**
- Django: Over-engineered for small household app, slower development, ORM overhead unnecessary
- Flask: Not built for async operations; websocket support requires add-on complexity
- **FastAPI wins**: Async-first, fastest request handling, cleaner code

### Database

| Technology | Version | Purpose | Why |
|-----------|---------|---------|-----|
| **SQLite** | 3.51.3 (March 2026) | Primary Database | Perfect for household app (two users, single household scope). No server required, file-based, transactions supported, ACID-compliant. Will store all events, recurring rules, user data. |
| **SQLAlchemy** | 2.x | ORM | Lightweight Python ORM, excellent type hints, works seamlessly with FastAPI, supports SQLite migrations via Alembic. |

**Why NOT PostgreSQL for v1:**
- SQLite sufficient for two users on same household network
- Zero infrastructure overhead
- Can upgrade to PostgreSQL later if multi-household sync needed

### Google Calendar Integration

| Library | Version | Purpose | Why |
|---------|---------|---------|-----|
| **google-api-python-client** | 2.193.0 | OAuth2 + Calendar API | Official Google client library, supports OAuth2 flow (two-user model), event CRUD operations, recurring events, full Calendar v3 API coverage. Discovery documents now cached (v2.x benefit). |
| **PyJWT** | Latest | Token Management | Parse/verify OAuth2 tokens for session management. |
| **python-dotenv** | Latest | Config Management | Store OAuth2 credentials safely in environment variables. |

### Frontend Approach

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Jinja2Templates** (Built into FastAPI/Starlette) | Server-side HTML rendering | For v1, use server-rendered HTML forms with HTMX for lightweight interactivity. No JavaScript framework build step needed. Reduces complexity. |
| **HTMX** | 1.9.x | Lightweight JavaScript | Progressive enhancement for forms (add event, edit event, delete). Real-time calendar updates without full page reloads. Integrates cleanly with Jinja2. |
| **Tailwind CSS** | 3.x | Styling | Utility-first CSS, ships lean, handles responsive calendar view. Or Bootstrap 5 if less hip. |

**Why this approach:**
- **v1 focus**: Two users on households network = no need for complex SPA
- **Server-side rendering** simplifies date parsing, recurring rule validation (all server-side)
- **HTMX**: Progressive enhancement, real-time event updates without WebSocket complexity
- **Future upgrade**: To React/Vue if multi-tenancy added

### Real-Time Updates Strategy

| Mechanism | Use Case | Why |
|-----------|----------|-----|
| **polling (5-10 sec intervals)** | Initial implementation | Simple, works everywhere, no infrastructure. JS on page requests `GET /events/today` every 5 seconds. Sufficient for household calendar. |
| **Server-Sent Events (SSE)** | Later optimization if polling feels slow | Unidirectional server-to-client streaming, built into FastAPI, no WebSocket complexity. Better than polling, simpler than WebSockets. |
| **WebSockets** | Future: multi-household real-time collaboration | Only if scaling beyond two-person household. |

**Decision:** Start with polling, migrate to SSE in Phase 2 if needed.

### Image Processing & OCR

| Library | Version | Purpose | Implementation |
|---------|---------|---------|-----------------|
| **EasyOCR** | 1.7.2 | Optical Character Recognition | Extract event name + date from festival flyers, screenshots. Supports 80+ languages, PyTorch backend, async-friendly. |
| **Pillow** | Latest | Image Handling | Load, resize, preprocess images before OCR. |
| **opencv-python** | 4.x | Image Processing | If advanced preprocessing needed (rotation detection, skew correction). Optional for v1. |

**Why NOT Google Vision API:**
- EasyOCR: Off-line, no API costs, privacy (household data stays local)
- Google Vision: Cloud dependency, latency, cost for household app seems overkill
- Tesseract (pytesseract): Older, requires system library installation, harder deployment

**Implementation Note:** OCR optional for v1, can defer to Phase 2. Requires GPU for real-time (or CPU + 2-3 sec delay).

### Natural Language Processing

| Library | Version | Purpose | Implementation |
|---------|---------|---------|-----------------|
| **dateparser** | 1.3.0 | Natural Language Date Extraction | Convert "tomorrow at 3pm", "next Friday", "in 2 weeks" → datetime objects. Supports 200+ locales, relative dates, timezone handling. |
| **spaCy** | 3.7 | NLP Pipeline (optional) | Extract entities (person names, locations) from event descriptions. Supports NER (Named Entity Recognition). Use `en_core_web_sm` model (small, fast). Optional for v1. |
| **PyDantic** | v2.x | Validation | Validate parsed dates/times have valid ranges (e.g., not hour 25). |

**Why this stack:**
- **dateparser**: Best-in-class for relative dates ("in 3 weeks" → calendar math)
- **spaCy**: If later adding "Add meeting with John at work" → extract participant + location
- **LLM approach NOT recommended yet**: Overkill for household calendar, latency, API costs

**Implementation:** dateparser required for v1 (natural language event requests). spaCy optional Phase 2 feature.

### Authentication (Two-User Model)

| Technology | Purpose | Why |
|-----------|---------|-----|
| **OAuth2 (via Google)** | User Authentication | Both users log in via Google, FastAPI's built-in OAuth2 + Security classes handle JWT tokens. |
| **JWT** | Session Management | Stateless tokens, refresh tokens for persistent login (up to 7 days). |
| **FastAPI Security** | Route Protection | `@app.get("/events", dependencies=[Depends(get_current_user)])` ensures only authenticated users access calendar. |

**Two-User Setup:**
1. User A logs in via Google → gets JWT token
2. User B logs in via Google → gets JWT token  
3. Both are verified via `get_current_user()` dependency
4. All events stored under shared calendar ID (not per-user)
5. Authorization: Simple check that user A/B privilege matches calendar owner

**Why NOT local auth:**
- Google OAuth2 integrates with Google Calendar API (same credentials)
- No password hashing/storage overhead
- Both users must have Google accounts anyway (Google Calendar requirement)

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|------------|
| **python-multipart** | Latest | Form parsing | Handle multipart/form-data from image upload form. |
| **httpx** | Latest | HTTP requests | Used by google-api-python-client, test client in FastAPI. |
| **pytest** | Latest | Testing | Write unit tests for event creation, parsing, Google sync logic. |
| **freezegun** | Latest | Mock time in tests | Test recurring events, date edge cases. |
| **python-cron** | Latest (APScheduler) | Background jobs | Export calendar to Google on interval (every hour), sync back. |

### Installation Command

```bash
# Core
pip install fastapi[standard] uvicorn pydantic sqlalchemy alembic

# Google Calendar
pip install google-api-python-client PyJWT python-dotenv

# Frontend
pip install jinja2

# OCR + NLP
pip install easyocr dateparser spacy pillow opencv-python

# Supporting
pip install python-multipart httpx pytest freezegun apscheduler

# Development
pip install black flake8 mypy pytest-cov
```

## Frontend Approach: Server-Side Rendering vs SPA

| Aspect | SSR (Jinja2 + HTMX) | SPA (React/Vue) |
|--------|-------------------|-----------------|
| Complexity | Low | High |
| Bundle size | Minimal | 50KB+ gzipped |
| Time to first render | Instant | 2-3 sec (JS download) |
| Real-time updates | Polling / HTMX / SSE | WebSocket / REST |
| Deployment | Python only | Node.js build step |
| **Decision for v1** | ✅ Chosen | Later if needed |

**SSR Strategy:**
- `/` → Jinja2 renders calendar month view + event list
- `/add-event` → Form POST → server validates → returns updated calendar HTML (HTMX swap)
- `/events/api` → JSON endpoint for HTMX to fetch updates
- JavaScript minimal: HTMX for forms, vanilla JS for calendar interactions

## Alternatives Not Recommended

### Framework Alternatives
- **Starlette** _(too low-level, use FastAPI instead)_
- **Django** _(over-engineered, slower development)_
- **Flask** _(not async-first, requires add-ons for websockets)_

### Database
- **PostgreSQL** _(overkill for household v1, upgrade path exists)_
- **MongoDB** _(no relational structure needed for events, don't use)_

### OCR
- **Google Cloud Vision API** _(privacy concern, costs, latency)_
- **Tesseract + pytesseract** _(older, system dependency, harder deployment)_

### NLP
- **LLMs (GPT-4 API)** _(expensive, latency, overkill for simple date parsing)_
- **NLTK** _(older, less maintained than spaCy)_

### Frontend
- **Django Templates + jQuery** _(coupling, slower)_
- **Next.js** _(overkill for server-rendered calendar)_
- **Vue.js** _(good but unnecessary for v1 requirements)_

## Installation & Project Structure

```bash
# Create project
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Initialize database
alembic init app/migrations
alembic upgrade head

# Run development server
fastapi dev app/main.py
```

Project structure:
```
CalendarPlanner/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── database.py             # SQLAlchemy session
│   ├── models/                 # SQLAlchemy models (Event, User, Calendar)
│   ├── routes/                 # API endpoints (events, auth, sync)
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic (Google sync, date parsing)
│   │   ├── google_calendar.py # OAuth2, event sync
│   │   ├── date_parser.py     # dateparser integration
│   │   ├── ocr.py             # EasyOCR integration
│   ├── templates/              # Jinja2 HTML templates
│   ├── static/                 # CSS, minimal JS (HTMX)
│   └── migrations/             # Alembic schema migrations
├── tests/
│   ├── test_routes.py
│   ├── test_services.py
│   └── test_date_parsing.py
├── requirements.txt
├── .env                        # OAuth2 secrets (git-ignored)
└── docker-compose.yml          # Optional: for local development
```

## Google Calendar OAuth2 Flow

```
1. User clicks "Login with Google"
2. Redirect to Google consent screen
3. User authorizes calendar access
4. Google returns authorization code
5. FastAPI exchanges code for access + refresh tokens
6. Store refresh token in session
7. Use access token to call Google Calendar API
8. Auto-refresh token when expired
```

## Deployment Considerations

- **Local/Household:** Run on Raspberry Pi or home server (one instance, SQLite sufficient)
- **Cloud upgrade:** Render, Railway, or Docker container (no changes needed, SQLite → PostgreSQL only)
- **Environment:** Python 3.10+ required (for union types, match/case)

## Versions as of March 2026

| Technology | Version | Release Date |
|-----------|---------|--------------|
| FastAPI | 0.135.1 | January 2026 |
| SQLite | 3.51.3 | March 13, 2026 |
| google-api-python-client | 2.193.0 | March 17, 2026 |
| dateparser | 1.3.0 | February 2026 |
| EasyOCR | 1.7.2 | September 2024 |
| spaCy | 3.7 | Latest (v4 coming soon) |
| Python | 3.10+ | Current standard |

---

**Confidence Levels:**
- **Stack recommendation:** HIGH (all libraries current, well-maintained, widely used)
- **Frontend SSR approach:** MEDIUM-HIGH (suitable for v1, team may prefer SPA later)
- **OCR/NLP optional features:** MEDIUM (EasyOCR excellent but requires GPU optimization)
- **Two-user OAuth2 auth:** HIGH (Google's pattern, well-documented)

