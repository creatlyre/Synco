---
phase: 22
slug: historical-year-import
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-22
---

# Phase 22 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.4.3 |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/test_import.py -x -v` |
| **Full suite command** | `python -m pytest tests/ -x -v` |
| **Estimated runtime** | ~0.24 seconds (import tests) |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_import.py -x -v`
- **After every plan wave:** Run `python -m pytest tests/ -x -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 22-01-01 | 01 | 1 | IMP-01 | unit+integration | `pytest tests/test_import.py::test_bulk_hours_import_success -v` | ✅ | ✅ green |
| 22-01-01 | 01 | 1 | IMP-01 | unit | `pytest tests/test_import.py::test_bulk_hours_import_upsert -v` | ✅ | ✅ green |
| 22-01-01 | 01 | 1 | IMP-01 | unit | `pytest tests/test_import.py::test_bulk_hours_import_empty -v` | ✅ | ✅ green |
| 22-01-01 | 01 | 1 | IMP-01 | boundary | `pytest tests/test_import.py::test_bulk_hours_invalid_year -v` | ✅ | ✅ green |
| 22-01-02 | 01 | 1 | IMP-02 | integration | `pytest tests/test_import.py::test_imported_expenses_in_yoy -v` | ✅ | ✅ green |
| 22-01-02 | 01 | 1 | IMP-03 | integration | `pytest tests/test_import.py::test_imported_recurring_expenses_in_overview -v` | ✅ | ✅ green |
| 22-01-03 | 01 | 1 | IMP-04 | integration | `pytest tests/test_import.py::test_import_feeds_yoy_comparison -v` | ✅ | ✅ green |
| 22-01-02 | 01 | 1 | Route | smoke | `pytest tests/test_import.py::test_import_page_accessible -v` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Audit 2026-03-22

| Metric | Count |
|--------|-------|
| Gaps found | 3 |
| Resolved | 3 |
| Escalated | 0 |

### Gap Details

| # | Requirement | Gap Type | Resolution |
|---|-------------|----------|------------|
| 1 | IMP-03 (recurring expense import) | MISSING | Added `test_imported_recurring_expenses_in_overview` |
| 2 | IMP-01 (year validation boundary) | MISSING | Added `test_bulk_hours_invalid_year` |
| 3 | Route accessibility | MISSING | Added `test_import_page_accessible` |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 1s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-22
