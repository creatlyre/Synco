---
phase: 38
slug: gated-features-entitlements-e2e
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-25
---

# Phase 38 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright Test (TypeScript) |
| **Config file** | `playwright.config.ts` (from Phase 36) |
| **Quick run command** | `npx playwright test tests/e2e/test_gating.spec.ts --reporter=list` |
| **Full suite command** | `npx playwright test tests/e2e/test_gating.spec.ts tests/e2e/test_budget.spec.ts tests/e2e/test_shopping.spec.ts tests/e2e/test_sync.spec.ts --reporter=list` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick run command (gating tests)
- **After every plan wave:** Run full suite command
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 38-01-01 | 01 | 1 | GATE-E2E-01, GATE-E2E-02, GATE-E2E-03, GATE-E2E-04 | e2e | `npx playwright test tests/e2e/test_gating.spec.ts` | ❌ W0 | ⬜ pending |
| 38-01-02 | 01 | 1 | BUD-E2E-01, BUD-E2E-02, BUD-E2E-03, SHOP-E2E-01, SHOP-E2E-02 | e2e | `npx playwright test tests/e2e/test_budget.spec.ts tests/e2e/test_shopping.spec.ts` | ❌ W0 | ⬜ pending |
| 38-01-03 | 01 | 1 | SYNC-E2E-01, SYNC-E2E-02 | e2e | `npx playwright test tests/e2e/test_sync.spec.ts` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Phase 36 infrastructure complete (playwright.config.ts, auth storage states, projects)
- [ ] Phase 37 tests passing (core app E2E verifies auth and calendar work)

*Existing Phase 36 infrastructure covers all framework requirements.*

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
