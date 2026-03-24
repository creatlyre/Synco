---
phase: 04
slug: admin-dashboard-user-management-plan-assignment-admin-privileges-and-statistics
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-24
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/test_admin.py -x --tb=short` |
| **Full suite command** | `python -m pytest tests/test_admin.py -v --tb=short` |
| **Estimated runtime** | ~8 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_admin.py -x --tb=short`
- **After every plan wave:** Run `python -m pytest tests/test_admin.py -v --tb=short`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | ADM-01 | unit | `python -m pytest tests/test_admin.py -x --tb=short` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | ADM-01,ADM-02 | unit | `python -m pytest tests/test_admin.py -x --tb=short` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 2 | ADM-03,ADM-04 | unit | `python -m pytest tests/test_admin.py -x --tb=short` | ❌ W0 | ⬜ pending |
| 04-02-02 | 02 | 2 | ADM-03 | integration | `python -m pytest tests/test_admin.py -v --tb=short` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_admin.py` — stubs for ADM-01 through ADM-04
- [ ] Existing `tests/conftest.py` — shared fixtures (already present)

*Existing infrastructure covers test framework. Only test file creation needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Admin nav link visible only for admin users | ADM-01 | Visual UI check | Log in as admin, verify shield icon in nav. Log in as regular user, verify no admin link. |
| Admin dashboard stats cards render correctly | ADM-03 | Visual layout | Visit /admin, verify stat cards show user count, plan distribution |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
