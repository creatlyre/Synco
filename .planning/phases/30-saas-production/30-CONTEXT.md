# Phase 30: SaaS Production Platform and Operations - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the Synco FastAPI application production-ready for SaaS deployment: Dockerfile, hosting platform config (Railway), production ASGI server (gunicorn + uvicorn workers), environment-based configuration (staging + production), structured logging, error tracking (Sentry), enhanced health checks, and security hardening (CORS, rate limiting, security headers). This phase focuses on **deployment and operations infrastructure** — billing/entitlements were completed in Phase 29, self-hosted distribution belongs to Phase 31.

Requirements addressed: SAS-01.

</domain>

<decisions>
## Implementation Decisions

### Hosting Platform
- **Railway** as the deployment target for SaaS hosting.
- Rationale: simplest path for a solo developer, auto-TLS/HTTPS, built-in environment variable management, good Docker support, integrated logging, reasonable pricing for small SaaS.
- Two environments: **staging** and **production** as separate Railway services reading from the same Supabase project (staging) or separate Supabase projects.
- Custom domain support via Railway's domain settings.
- Stripe webhooks pointed at production domain (staging uses Stripe test mode).

### Production Server Configuration
- **Dockerfile** with multi-stage build: Python 3.12 base, install deps, copy app, run with gunicorn.
- **Gunicorn** with **uvicorn workers** (`-k uvicorn.workers.UvicornWorker`) — standard Python ASGI production setup.
- Worker count: `2 * CPU_CORES + 1` or configured via `WEB_CONCURRENCY` env var.
- `.dockerignore` to exclude tests, planning docs, `.git`, `__pycache__`, `.env`.
- `railway.toml` or `Procfile` for Railway deployment config.
- Environment variables managed via Railway dashboard (no `.env` files in production).
- `.env.example` file documenting all required env vars for developer reference.

### Observability Stack
- **Structured JSON logging** using Python's stdlib `logging` module with a JSON formatter for production (human-readable for development).
- Log level controlled via `LOG_LEVEL` env var (default: `INFO` in production, `DEBUG` in development).
- **Sentry** free tier for error tracking and performance monitoring (`sentry-sdk[fastapi]`).
- Sentry DSN configured via `SENTRY_DSN` env var — disabled in development if not set.
- Enhanced `/health` endpoint with DB connectivity check (Supabase ping) and Stripe API reachability.
- `/health/ready` readiness endpoint for Railway health checks.

### Security Hardening
- **CORS middleware** (`CORSMiddleware`) with allowlisted origins from `ALLOWED_ORIGINS` env var (comma-separated).
- **Rate limiting** via `slowapi` on sensitive endpoints: auth routes (login, register), billing routes (checkout, webhook), and API mutation endpoints.
- Rate limits: 10 req/min on auth endpoints, 20 req/min on billing endpoints, 60 req/min general API.
- **Security headers middleware**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security` (HSTS), `Referrer-Policy: strict-origin-when-cross-origin`.
- **CSRF protection** not needed — API uses JWT in cookies with SameSite attribute; Stripe webhooks use signature verification.
- `DEBUG=false` enforced in production (no auto-reload, no detailed error pages).

### Claude's Discretion
- Exact gunicorn configuration values (timeout, graceful-timeout, keep-alive).
- Sentry SDK configuration details (traces_sample_rate, environment tagging).
- Specific structure of the JSON log formatter.
- Railway service naming conventions.
- Whether to add a `/metrics` endpoint for basic app stats.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Billing Infrastructure (Phase 29)
- `.planning/phases/29-billing/29-CONTEXT.md` — Billing decisions: Stripe provider, plan model, entitlement architecture
- `.planning/phases/29-billing/29-01-SUMMARY.md` — Stripe checkout, webhook handler, billing events table
- `.planning/phases/29-billing/29-02-SUMMARY.md` — Entitlement dependencies, billing settings page

### Monetization & Licensing
- `MONETIZATION.md` — Free vs paid model, tier descriptions, SaaS vs self-hosted
- `COMMERCIAL-LICENSE.md` — Dual-license commercial terms
- `LICENSE` — AGPL-3.0 full text

### Requirements
- `.planning/REQUIREMENTS.md` — SAS-01 (hosted deployment path with staging + production)

### Application Entry Points
- `main.py` — FastAPI app setup, middleware, router registration, existing `/health` endpoint
- `config.py` — Settings class with all current env vars (Supabase, Google, Stripe, SMTP)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `main.py` `/health` endpoint: Basic health check exists, can be enhanced with DB + Stripe connectivity checks.
- `config.py` `Settings(BaseSettings)`: Pydantic-settings with `.env` support — extend with production config vars (SENTRY_DSN, ALLOWED_ORIGINS, LOG_LEVEL, WEB_CONCURRENCY).
- `StaticCacheMiddleware` in `main.py`: Pattern for custom middleware — can follow for security headers.
- `SessionValidationMiddleware`: Existing middleware pattern for request-level operations.

### Established Patterns
- **Pydantic-settings** `BaseSettings` with `SettingsConfigDict(env_file=".env", extra="ignore")` for config management.
- **FastAPI middleware** via `BaseHTTPMiddleware` for request/response processing.
- **SupabaseStore** for all DB operations via REST API (httpx pooled client).
- **Router modules** per domain registered in `main.py`.
- All environment variables currently: `SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `GOOGLE_CLIENT_ID/SECRET`, `DB_ENCRYPTION_KEY`, `SMTP_*`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_PRO_PRICE_ID`, `STRIPE_FAMILY_PLUS_PRICE_ID`.

### Integration Points
- `main.py` — Add CORS, rate limiting, security headers, and Sentry middleware.
- `config.py` — Add SENTRY_DSN, ALLOWED_ORIGINS, LOG_LEVEL, WEB_CONCURRENCY, ENVIRONMENT.
- `requirements.txt` — Add `gunicorn`, `sentry-sdk[fastapi]`, `slowapi`.
- New files: `Dockerfile`, `.dockerignore`, `railway.toml` or `Procfile`, `.env.example`, `app/middleware/security.py`.

</code_context>

<specifics>
## Specific Ideas

- Railway deployment with auto-deploy from main branch (staging from develop if branch exists, production from main).
- Stripe webhook URL in production: `https://{custom-domain}/api/billing/webhook` — documented in `.env.example`.
- Sentry environment tag: `production` or `staging` derived from `ENVIRONMENT` env var.
- Health check response includes version from `pyproject.toml` for deployment verification.
- Production logging: JSON one-line per log entry, includes request_id for tracing.

</specifics>

<deferred>
## Deferred Ideas

- CI/CD pipeline with automated tests (could be a separate phase or part of go-to-market).
- Blue-green deployments or canary releases — overkill for household SaaS at launch.
- APM (Application Performance Monitoring) beyond Sentry basics — not needed at this scale.
- CDN for static assets — Railway handles this adequately for now.
- Auto-scaling beyond Railway's built-in scaling — premature optimization.
- Database connection pooling via PgBouncer — using Supabase REST API, not direct Postgres.

</deferred>

---

*Phase: 30-saas-production*
*Context gathered: 2026-03-23*
