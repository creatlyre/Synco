---
phase: 37
slug: core-app-e2e-tests
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-25
---

# Phase 37 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright (`@playwright/test`) — installed in Phase 36 |
| **Config file** | `e2e/playwright.config.ts` |
| **Quick run command** | `npx playwright test --config=e2e/playwright.config.ts --project=pro` |
| **Full suite command** | `npx playwright test --config=e2e/playwright.config.ts` |
| **Estimated runtime** | ~60-90 seconds (network round trips to Railway) |

---

## Sampling Rate

- **After every task commit:** Run `npx playwright test --config=e2e/playwright.config.ts --project=pro`
- **After every plan wave:** Run `npx playwright test --config=e2e/playwright.config.ts`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 90 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 37-01-01 | 01 | 1 | AUTH-E2E-01, AUTH-E2E-02, AUTH-E2E-03, AUTH-E2E-04 | e2e | `npx playwright test e2e/tests/test_auth.spec.ts --config=e2e/playwright.config.ts` | ❌ W0 | ⬜ pending |
| 37-02-01 | 02 | 1 | CAL-E2E-01, CAL-E2E-02, CAL-E2E-03 | e2e | `npx playwright test e2e/tests/test_calendar.spec.ts --config=e2e/playwright.config.ts` | ❌ W0 | ⬜ pending |
| 37-02-02 | 02 | 1 | DASH-E2E-01, DASH-E2E-02, DASH-E2E-03 | e2e | `npx playwright test e2e/tests/test_dashboard.spec.ts --config=e2e/playwright.config.ts` | ❌ W0 | ⬜ pending |
| 37-02-03 | 02 | 1 | NOTF-E2E-01, NOTF-E2E-02 | e2e | `npx playwright test e2e/tests/test_notifications.spec.ts --config=e2e/playwright.config.ts` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Phase 36 must be complete (Playwright installed, auth.setup.ts working, smoke test passing)
- [ ] `e2e/tests/test_auth.spec.ts` — auth flow E2E tests
- [ ] `e2e/tests/test_calendar.spec.ts` — calendar view E2E tests
- [ ] `e2e/tests/test_dashboard.spec.ts` — dashboard E2E tests
- [ ] `e2e/tests/test_notifications.spec.ts` — notification UI E2E tests
