---
phase: 36-e2e-test-infrastructure
plan: 02
subsystem: infra
tags: [github-actions, ci, playwright, e2e]

requires:
  - phase: 36-01
    provides: Playwright config and test files
provides:
  - GitHub Actions E2E workflow running on PRs to main
affects: [37-billing-e2e-tests, 38-gated-features-entitlements-e2e, 39-cross-role-e2e]

tech-stack:
  added: []
  patterns: ["non-blocking CI E2E gate", "secret-injected Playwright CI"]

key-files:
  created:
    - .github/workflows/e2e.yml
  modified: []

key-decisions:
  - "Non-blocking (continue-on-error: true) until suite stabilizes"
  - "PR to main only — not every push or scheduled"
  - "Chromium-only with --with-deps for OS-level dependencies"
  - "14-day artifact retention for screenshots and traces"
  - "10-minute timeout for network-bound tests"

patterns-established:
  - "E2E CI: checkout → setup-node → npm ci → install chromium → run tests → upload artifacts"
  - "All E2E secrets injected via GitHub Actions secrets (7 vars)"

requirements-completed: [INFRA-05]

duration: 3min
completed: 2026-03-25
---

# Plan 36-02: GitHub Actions E2E Workflow

**CI workflow runs Playwright tests on PR to main with secret injection, Chromium install, and artifact upload on failure**

## Performance

- **Duration:** 3 min
- **Tasks:** 1/1
- **Files created:** 1

## Accomplishments
- GitHub Actions workflow triggers on PR to main
- Installs Chromium with OS-level dependencies for headless execution
- Injects all 7 E2E secrets (base URL + 3 account credentials)
- Uploads test-results/ and playwright-report/ as artifacts (14-day retention)
- Non-blocking (continue-on-error) until suite stabilizes

## Task Commits

1. **Task 1: Create GitHub Actions E2E workflow** — `2caa555` (feat)

## Files Created/Modified
- `.github/workflows/e2e.yml` — E2E CI workflow with Playwright, secrets, and artifact upload
