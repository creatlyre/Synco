# Phase 39: Billing, Stripe & Error Resilience E2E - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Pricing page rendering, checkout flow initiation (API-level), billing settings display, Stripe portal access, and error/auth-failure handling — all verified in the browser. This is the final phase of v5.1 E2E milestone. No real Stripe payments are made.

</domain>

<decisions>
## Implementation Decisions

### Checkout Flow Verification (API-Level Only)
- The pricing page JS `checkout()` function calls `POST /api/billing/checkout` with `{plan, billing_period}` → returns `{"url": "https://checkout.stripe.com/..."}`
- Tests call the checkout API via Playwright's `request` context (authenticated pro user) and verify:
  1. Response is 200 with JSON body containing a `url` field
  2. The URL starts with `https://checkout.stripe.com/`
- Test at least `pro` and `family_plus` plans (both monthly default)
- Do NOT follow the Stripe redirect or interact with Stripe Checkout page — that's Stripe's domain
- Do NOT test `self_hosted` checkout unless trivially easy (same pattern, different success URL)
- This matches roadmap success criteria: "Checkout API returns a valid checkout.stripe.com URL (redirect verified, payment form not submitted)"

### Pricing Page Rendering (Auth + Unauth)
- **Unauthenticated visitors:** Pricing page (`/pricing`) renders with plan cards (Free, Pro, Family+), monthly/annual toggle, and login/signup links — no checkout buttons should trigger checkout (API requires auth)
- **Authenticated users:** Same page renders with checkout buttons that are functional (Pro, Family+, self-hosted) — use `pro` project to verify buttons exist
- Verify both states: navigate to `/pricing` without auth (new browser context) and with auth (pro storage state)
- Plan card count: verify at least 3 visible plan sections (Free, Pro, Family+)

### Billing Settings & Portal Assertions
- **Pro user (`pro` project):**
  - `/billing/settings` loads with 200 status
  - Current plan section shows "Pro" plan label
  - Status badge shows "Active" (or equivalent)
  - "Manage subscription" button (`#manage-sub-btn`) is visible
  - `POST /api/billing/portal` returns 200 with `{"url": "https://billing.stripe.com/..."}` — verify URL prefix, don't follow
- **Free user (`free` project):**
  - `/billing/settings` loads with 200 status
  - Current plan shows "Free" plan label
  - "Manage subscription" button is NOT visible (no Stripe customer for free users)
  - `POST /api/billing/portal` returns 400 with `{"detail": "No billing account found"}`

### Error & Auth Failure Scenarios
- **Unauthenticated page access:** Navigate to `/billing/settings` and `/dashboard` without auth → verify redirect to `/auth/login` (302 from exception handler)
- **API without auth:** Call `POST /api/billing/checkout` without cookies → verify 401 response with `{"detail": "Not authenticated"}`
- **API invalid payload:** Call `POST /api/billing/checkout` with `{"plan": "invalid_plan"}` → verify 422 (Pydantic validation) or 400 error response
- **Portal without subscription:** Free user calls `POST /api/billing/portal` → verify 400 + error detail (already covered in billing settings section)
- **Skip rate limiting tests** — timing-dependent, flaky in E2E, not in scope
- **Skip expired session tests** — would require invalidating a real Supabase session, too complex for read-only E2E

### Test Data Strategy
- Consistent with Phases 37-38: **all tests are read-only / non-destructive**
- Checkout API is called but the returned Stripe URL is never visited — no actual checkout session is consumed
- Portal API is called but the returned Stripe URL is never visited — no billing changes
- No plan changes, no subscription mutations

### Test File Organization
- `e2e/tests/test_billing.spec.ts` — Pricing page (auth + unauth), billing settings (pro + free), checkout API, portal API
- `e2e/tests/test_errors.spec.ts` — Auth redirect for unauthenticated access, API error responses (401, 400/422)
- Keep billing and error tests separate — different concerns, different Playwright projects needed

### Claude's Discretion
- Whether to combine pricing unauth test with error tests or keep in billing file
- Exact assertions for plan card content (CSS selectors, text matching)
- Whether to test annual billing period in checkout API (monthly is sufficient)
- How to create an unauthenticated browser context (new `browser.newContext()` or separate project)
- Test describe/it naming conventions

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase dependencies
- `.planning/phases/36-e2e-test-infrastructure/36-CONTEXT.md` — Playwright setup, projects (free/pro/family-plus), auth strategy, CI config
- `.planning/phases/37-core-app-e2e-tests/37-CONTEXT.md` — Read-only test pattern, test file conventions
- `.planning/phases/38-gated-features-entitlements-e2e/38-CONTEXT.md` — Gating pattern, upgrade redirect verification

### Billing API
- `app/billing/routes.py` — `POST /api/billing/checkout` (returns Stripe URL), `POST /api/billing/portal` (returns portal URL), `POST /api/billing/webhook`
- `app/billing/schemas.py` — `CheckoutRequest` pydantic model: `{plan: str, billing_period: "monthly"|"annual"}`, `VALID_PLANS = ("pro", "family_plus", "self_hosted")`
- `app/billing/views.py` — `GET /pricing` (public), `GET /billing/settings` (authenticated)
- `app/billing/service.py` — `BillingService.create_checkout_session()`, `create_portal_session()`

### Templates
- `app/templates/pricing.html` — Plan cards (Free, Pro, Family+, self-hosted), monthly/annual toggle, `checkout(plan)` JS function calling `/api/billing/checkout`
- `app/templates/billing_settings.html` — Current plan display, status badge, `#manage-sub-btn` button, JS calling `/api/billing/portal`

### Error handling
- `main.py` lines 333-343 — `auth_redirect_handler`: 401 on `/invite`,`/dashboard` → 302 to `/auth/login`; 403 on `/admin/*` → 302 to `/dashboard`
- `app/auth/dependencies.py` — `get_current_user()` raises `HTTPException(401)` for missing/invalid sessions

### Auth flow
- `app/auth/dependencies.py` — `get_current_user()` reads session cookies, raises 401 if invalid
- `app/billing/dependencies.py` — `require_plan()` raises `UpgradeRedirect` or 403 for gated features

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Playwright projects `free`, `pro`, `family-plus` with pre-authenticated storage states (Phase 36)
- Existing E2E test patterns from Phases 37-38: `page.goto()` + status check + element assertions
- `page.request` API for making authenticated API calls within Playwright tests

### Key Selectors (from templates)
- Pricing page: `checkout('pro')` / `checkout('family_plus')` / `checkout('self_hosted')` onclick handlers
- Pricing plan cards: no specific IDs but cards have `h3` headings with plan names
- Billing settings: `#manage-sub-btn` for manage subscription button
- Monthly/annual toggle: `#billing-toggle` checkbox, `#pro-price` / `#fp-price` price display spans

### API Response Patterns
- Checkout success: `{"url": "https://checkout.stripe.com/c/pay/..."}`
- Portal success: `{"url": "https://billing.stripe.com/p/session/..."}`
- Portal no subscription: `400 {"detail": "No billing account found"}`
- Auth failure: `401 {"detail": "Not authenticated"}`
- Invalid plan: `422` (Pydantic validation error) with standard FastAPI error format

### Established Patterns
- Server-rendered Jinja2 + HTMX — pricing page is fully server-rendered, checkout is client-side JS
- Polish as default locale — plan names and labels will be in Polish (use i18n keys from `en.json`/`pl.json`)
- `get_current_user` raises 401 → caught by `auth_redirect_handler` for certain paths, passes through as JSON 401 for API paths

</code_context>

<specifics>
## Specific Ideas

- Use Playwright's `request` context (not `page.evaluate(fetch(...))`) for API-level tests — cleaner and doesn't depend on page JS
- For unauthenticated tests, create a fresh browser context without storage state rather than a separate Playwright project
- Pricing page rendering test should verify the monthly/annual toggle switches displayed prices
- The pro user's billing settings should show a recognizable plan indicator — match against known i18n strings or CSS classes

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 39-billing-stripe-error-resilience-e2e*
*Context gathered: 2026-03-25*
