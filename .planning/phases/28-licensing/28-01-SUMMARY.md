---
phase: 28-licensing
plan: 01
subsystem: legal
tags: [agpl, dual-license, monetization, commercial-license]

requires: []
provides:
  - COMMERCIAL-LICENSE.md with dual-license terms (SaaS + self-hosted)
  - MONETIZATION.md explaining free vs paid model with FAQ
  - NOTICE file with copyright and third-party attributions
affects: [28-02, 29-billing, 33-launch]

tech-stack:
  added: []
  patterns:
    - "Dual-license documentation pattern: AGPL-3.0 core + commercial exception"

key-files:
  created:
    - COMMERCIAL-LICENSE.md
    - MONETIZATION.md
    - NOTICE
  modified: []

key-decisions:
  - "Used informational-not-legal-contract approach for COMMERCIAL-LICENSE.md"
  - "Included comparison table in MONETIZATION.md for SaaS vs self-hosted"
  - "Deferred pricing specifics to Phase 33 (GTM)"

patterns-established:
  - "Licensing docs pattern: COMMERCIAL-LICENSE.md for terms, MONETIZATION.md for model explanation, NOTICE for attribution"

requirements-completed:
  - MON-02
  - MON-03

duration: 5min
completed: 2026-03-23
---

# Plan 28-01: Licensing and Monetization Core Documents

**Established Synco's dual-license documentation with commercial terms, monetization model, and third-party attribution.**

## Performance

- **Duration:** 5 min
- **Tasks:** 2/2 completed
- **Files created:** 3

## Accomplishments
- Created COMMERCIAL-LICENSE.md covering SaaS subscription and self-hosted one-time purchase paths
- Created MONETIZATION.md with clear free/paid breakdown, AGPL obligation summary, comparison table, and FAQ
- Created NOTICE file with copyright and all third-party dependency licenses

## Task Commits

1. **Task 1: Create COMMERCIAL-LICENSE.md and NOTICE file** — `84c4bc0` (feat)
2. **Task 2: Create MONETIZATION.md** — `e390643` (feat)

## Files Created/Modified
- `COMMERCIAL-LICENSE.md` — Dual-license commercial terms (who needs it, what it grants, self-hosted details, purchase info)
- `MONETIZATION.md` — Free vs paid explanation, AGPL obligations in plain language, SaaS vs self-hosted comparison table, FAQ
- `NOTICE` — Copyright attribution and third-party dependency license list

## Decisions Made
- Used placeholder for pricing page (deferred to Phase 33 GTM)
- Used licensing@synco.app as contact email across all docs
- Included a comparison table in MONETIZATION.md for quick SaaS vs self-hosted scanning

## Deviations from Plan
None — plan executed exactly as written.

## Issues Encountered
None.
