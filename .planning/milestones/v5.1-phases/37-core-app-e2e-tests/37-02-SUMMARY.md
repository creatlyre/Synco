---
phase: 37-core-app-e2e-tests
plan: 02
subsystem: testing
tags: [playwright, e2e, dashboard, notifications, htmx]

requires:
  - phase: 36-e2e-test-infrastructure
    provides: Playwright config, auth setup, CI pipeline

provides:
  - Dashboard E2E tests (redirect, sections, quick-add link)
  - Notification UI E2E tests (bell icon, dropdown load)

affects: [39-error-resilience-e2e]

tech-stack:
  added: []
  patterns: [networkidle wait for server-rendered pages, Promise.all for click+waitForResponse]

key-files:
  created:
    - e2e/tests/test_dashboard.spec.ts
    - e2e/tests/test_notifications.spec.ts

key-decisions:
  - "Dashboard sections verified by CSS class selectors (.glass cards, h2.text-section-title) not i18n text"
  - "Notification dropdown verified via #notification-panel visibility after HTMX load"
  - "Promise.all pattern for concurrent click + waitForResponse to avoid race conditions"

patterns-established:
  - "Server-rendered page wait: waitForLoadState('networkidle') before DOM assertions"
  - "HTMX click+load: Promise.all([waitForResponse, click]) to avoid race"
  - "Section count assertions: .glass card count ≥ 2 verifies dashboard fully rendered"

requirements-completed: [DASH-E2E-01, DASH-E2E-02, DASH-E2E-03, NOTF-E2E-01, NOTF-E2E-02]

duration: 6min
completed: 2026-03-25
---

# Plan 37-02: Dashboard + Notification E2E Tests Summary

**3 dashboard E2E tests and 2 notification UI E2E tests covering page load, sections, and bell dropdown**

## Performance

- **Duration:** 6 min
- **Tasks:** 2
- **Files created:** 2 (test_dashboard.spec.ts, test_notifications.spec.ts)

## Accomplishments
- Dashboard tests: root `/` redirects to `/dashboard`, today's events heading visible, quick-add link and glass cards present
- Notification tests: bell icon visible in navbar, clicking bell triggers HTMX load of dropdown
- All tests are read-only — no production data mutations

## Task Commits

1. **Task 1: Dashboard E2E tests** — `0bc1114` (test)
2. **Task 2: Notification UI E2E tests** — `0bc1114` (test, same commit)

## Files Created/Modified
- `e2e/tests/test_dashboard.spec.ts` — 3 dashboard tests (redirect, events section, budget + quick-add)
- `e2e/tests/test_notifications.spec.ts` — 2 notification tests (bell visible, dropdown loads)

## Decisions Made
- Used CSS selector-based assertions instead of Polish text matching for i18n resilience
- Notification dropdown assertion uses `#notification-panel` visibility (the HTMX target container)
- Used `Promise.all` for click+waitForResponse to prevent race condition with HTMX

## Deviations from Plan
None - plan executed as written.

## Issues Encountered
- E2E env vars not available locally — tests verified via `--list` compilation check. Full runtime verification requires CI.

## Next Phase Readiness
- All 12 core app E2E tests ready for CI execution
- Patterns established for HTMX interaction testing

---
*Phase: 37-core-app-e2e-tests*
*Completed: 2026-03-25*
