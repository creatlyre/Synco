---
phase: 36
slug: e2e-test-infrastructure
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-25
validated: 2026-03-25
---

# Phase 36 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | @playwright/test (Node.js) |
| **Config file** | e2e/playwright.config.ts |
| **Quick run command** | `npx playwright test --project=setup` |
| **Full suite command** | `npx playwright test` |
| **Estimated runtime** | ~30 seconds (network-bound against Railway) |

---

## Sampling Rate

- **After every task commit:** Run `npx playwright test --project=setup`
- **After every plan wave:** Run `npx playwright test`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 36-01-01 | 01 | 1 | INFRA-01 | config | `test -f e2e/playwright.config.ts` | ✅ | ✅ green |
| 36-01-02 | 01 | 1 | INFRA-02 | e2e | `npx playwright test --project=setup` | ✅ | ✅ green |
| 36-02-01 | 02 | 2 | INFRA-03, INFRA-04 | e2e | `npx playwright test` | ✅ | ✅ green |
| 36-02-02 | 02 | 2 | INFRA-05 | config | `cat .github/workflows/e2e.yml` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `e2e/playwright.config.ts` — Playwright config with setup project and 3 role projects
- [x] `e2e/auth.setup.ts` — Login all 3 accounts and save storage state
- [x] `@playwright/test` devDependency — installed

*All Wave 0 requirements satisfied.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| GitHub Actions secrets configured | INFRA-05 | Secrets stored in GitHub dashboard | Verify E2E_* secrets exist in repo Settings > Secrets |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-03-25

---

## Validation Audit 2026-03-25

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

All 5 requirements (INFRA-01 through INFRA-05) verified against on-disk artifacts. Commits confirmed: `6458d52`, `0785397`, `2caa555`.
