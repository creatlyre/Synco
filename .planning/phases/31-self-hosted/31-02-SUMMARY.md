---
phase: 31-self-hosted
plan: 02
subsystem: docs, testing
tags: [self-hosted, documentation, license-tests, setup-guide]

requires:
  - phase: 31-self-hosted plan 01
    provides: License key module, Docker Compose package

provides:
  - Buyer-facing setup guide (README)
  - Upgrade and rollback procedure
  - Self-hosted changelog
  - License key test suite (18 tests)

affects: []

tech-stack:
  added: []
  patterns: [self-hosted documentation structure]

key-files:
  created:
    - self-hosted/README.md
    - self-hosted/UPGRADE.md
    - self-hosted/CHANGELOG-SELFHOSTED.md
    - tests/test_licensing.py
  modified: []

key-decisions:
  - "README covers prerequisites through first login with config reference table"
  - "Upgrade docs include backup-first pattern and rollback procedure"
  - "18 tests covering generation, validation (including edge cases), and middleware"

patterns-established:
  - "Self-hosted documentation in self-hosted/ directory"
  - "License tests with isolated test apps for middleware behavior"

requirements-completed: [SHS-03, SHS-04]

duration: 5min
completed: 2026-03-23
---

# Plan 31-02: Setup Guide, Upgrade Docs, and License Tests

**Buyer-facing self-hosted documentation and 18-test license key suite**

## Performance

- **Duration:** 5 min
- **Tasks:** 2/2
- **Files created:** 4

## Accomplishments

- `self-hosted/README.md`: Setup guide covering prerequisites, 5-step quick start, full config reference, Google Calendar / SMTP / HTTPS sections, backup/restore, architecture diagram, troubleshooting
- `self-hosted/UPGRADE.md`: Standard upgrade (pull + down + up), automatic DB migrations, rollback from backup
- `self-hosted/CHANGELOG-SELFHOSTED.md`: v4.0.0 initial release with feature list and known limitations
- `tests/test_licensing.py`: 18 tests — key generation (format, uniqueness, deterministic validation), key validation (valid, wrong secret, malformed, tampered, None, integer), middleware (skips non-self-hosted, valid key no banner, invalid key shows banner, missing key shows banner, skips health, skips JSON API)

## Self-Check: PASSED
- All 18 tests pass ✓
- README has docker compose up, .env.template, SYNCO_LICENSE_KEY references ✓
- UPGRADE has docker compose pull and backup instructions ✓
- CHANGELOG has v4.0 entry ✓
