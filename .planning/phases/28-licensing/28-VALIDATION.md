---
phase: 28
slug: licensing
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-23
---

# Phase 28 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x (existing) |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/ -x -q` |
| **Full suite command** | `python -m pytest tests/` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -q`
- **After every plan wave:** Run `python -m pytest tests/`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 28-01-01 | 01 | 1 | MON-01 | file check | `Select-String "AFFERO" LICENSE` | ✅ | ✅ green |
| 28-01-02 | 01 | 1 | MON-02 | file check | `Test-Path COMMERCIAL-LICENSE.md` | ✅ | ✅ green |
| 28-02-01 | 02 | 1 | MON-03 | file check | `Test-Path MONETIZATION.md` | ✅ | ✅ green |
| 28-02-02 | 02 | 1 | MON-03 | content | `Select-String "free|paid" README.md` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. Phase 28 is documentation-only — no new test files needed. Verification is file existence and content checks.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Commercial terms are legally reasonable | MON-02 | Requires human judgment | Review COMMERCIAL-LICENSE.md for clarity and accuracy |
| Monetization docs are understandable | MON-03 | Requires human reading | Read MONETIZATION.md — is it clear what's free vs paid? |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-23

---

## Validation Audit 2026-03-23

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

All file checks verified green. Phase 28 is documentation-only — no new test files needed.
