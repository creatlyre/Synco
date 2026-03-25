---
phase: 39-billing-stripe-error-resilience-e2e
plan: 02
subsystem: testing
tags: [playwright, e2e, auth, middleware, validation, error-handling]

requires:
  - phase: 36-e2e-test-infrastructure
    provides: Playwright config, auth setup, storage states
  - phase: 38-gated-features-entitlements-e2e
    provides: storageState override pattern, API request pattern

provides:
  - Auth redirect E2E tests for unauthenticated access to protected pages
  - Middleware rejection test with maxRedirects:0 for API endpoints
  - Pydantic validation error test (422) for invalid checkout payload

affects: [e2e, auth, middleware, billing]

tech-stack:
  added: []
  patterns:
    - "maxRedirects: 0 on page.request to capture middleware 302 redirect without following"
    - "SessionValidationMiddleware test pattern: verify 302 redirect to /auth/login for protected routes"

key-files:
  created:
    - e2e/tests/test_errors.spec.ts
  modified: []

key-decisions:
  - "Discovered SessionValidationMiddleware intercepts ALL non-public routes before route handler — 302 redirect, not 401"
  - "Used maxRedirects: 0 to verify API middleware rejection returns 302 + location header"
  - "Validation test uses authenticated pro context to reach past middleware to Pydantic validator"

patterns-established:
  - "maxRedirects: 0 for testing middleware redirects on API endpoints"
  - "SessionValidationMiddleware awareness: unauthenticated requests get 302 not 401"

requirements-completed: [ERR-E2E-01, ERR-E2E-02, ERR-E2E-03]

duration: ~15min
completed: 2025-07-15
---

# Plan 39-02: Error Resilience E2E Tests Summary

**Auth redirect, middleware rejection, and payload validation E2E tests against live deployment**

## Performance

- **Tasks:** 1 completed
- **Files created:** 1 (e2e/tests/test_errors.spec.ts — 55 lines)
- **Test results:** 15/15 pass (4 tests × 3 projects + 3 setup)

## Accomplishments
- Unauthenticated `/dashboard` correctly redirects to `/auth/login`
- Unauthenticated `/billing/settings` correctly redirects to `/auth/login` via SessionValidationMiddleware
- API POST `/api/billing/checkout` without auth returns 302 redirect (middleware level, not 401)
- API POST with `{ plan: 'invalid_plan' }` returns 422 Pydantic validation error

## Task Commits

1. **Task 1: Error resilience E2E tests** — `acd8ff5` (test, combined commit with 39-01)

## Files Created/Modified
- `e2e/tests/test_errors.spec.ts` — 4 tests across 3 describe blocks: Auth Redirects (2), API Error Responses (1), API Validation Errors (1)

## Decisions Made
- **Middleware-first auth:** Discovered that `SessionValidationMiddleware` catches ALL non-public routes and returns 302 redirect BEFORE FastAPI route handlers run. This means unauthenticated API calls get 302 (not 401), and protected pages always redirect (even those not in the exception handler's path set).
- **maxRedirects: 0:** Used `page.request.post(..., { maxRedirects: 0 })` to capture the raw 302 response for API tests, verifying the redirect location header includes `/auth/login`.

## Deviations from Plan

### Auto-fixed Issues

**1. Billing settings expected 401, got 302→200**
- **Found during:** First test run
- **Issue:** Plan assumed `/billing/settings` would return 401 (not in exception handler path set). Actually, `SessionValidationMiddleware` catches it first and returns 302 to `/auth/login`.
- **Fix:** Changed test to verify redirect to `/auth/login` using `page.waitForURL`
- **Verification:** Test passes for all projects

**2. API expected 401, got 302→200**
- **Found during:** First test run
- **Issue:** `page.request.post` follows redirects by default. With 302→GET `/auth/login`→200, the final status was 200.
- **Fix:** Added `maxRedirects: 0` to get raw 302 response; assert status 302 + location header
- **Verification:** Test passes for all projects

**Total deviations:** 2 auto-fixed (middleware behavior discovery)
**Impact on plan:** ERR-E2E-01 and ERR-E2E-02 requirements still met — unauthenticated access is properly rejected. The rejection mechanism is 302 redirect (middleware) rather than 401 JSON (route handler).

## Issues Encountered
None — once middleware behavior was understood, all tests passed on first re-run.

## Next Phase Readiness
- All Phase 39 plans complete
- Phase 39 can be verified and closed

---
*Phase: 39-billing-stripe-error-resilience-e2e, Plan: 02*
*Completed: 2025-07-15*
