---
phase: 08
slug: localization-foundation-and-polish-default
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-20
---

# Phase 08 — Validation Strategy

> Per-phase validation contract for localization foundation and Polish default.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.4.3 |
| **Config file** | pyproject.toml |
| **Quick run command** | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py -q` |
| **Full suite command** | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py tests/test_auth.py tests/test_events_api.py -q` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py -q`
- **After every plan wave:** Run `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py tests/test_auth.py tests/test_events_api.py -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | I18N-01, I18N-04 | integration | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py -k "calendar or invite" -q` | ✅ | ✅ green |
| 08-01-02 | 01 | 1 | I18N-01, I18N-04 | integration | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py tests/test_auth.py -k "calendar or invite or login" -q` | ✅ | ✅ green |
| 08-02-01 | 02 | 2 | I18N-04 | integration | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py -k "quick_add or invite or month or day" -q` | ✅ | ✅ green |
| 08-02-02 | 02 | 2 | I18N-04 | integration | `.venv\Scripts\python.exe -m pytest tests/test_auth.py tests/test_events_api.py tests/test_users.py -k "message or detail or invalid" -q` | ✅ | ✅ green |
| 08-03-01 | 03 | 3 | I18N-01, I18N-05 | integration | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py -k "month or day or quick_add" -q` | ✅ | ✅ green |
| 08-03-02 | 03 | 3 | I18N-01, I18N-05 | integration | `.venv\Scripts\python.exe -m pytest tests/test_calendar_views.py tests/test_events_api.py -q` | ✅ | ✅ green |

---

## Requirement Coverage

| Requirement | Description | Tests | Status |
|-------------|-------------|-------|--------|
| I18N-01 | Polish UI copy by default | `test_default_locale_is_polish` — asserts `lang="pl"` and Polish labels (Kalendarz, Wyloguj, Synchronizacja Google) | ✅ COVERED |
| I18N-04 | Labels in both Polish and English | `test_default_locale_is_polish` (Polish), `test_switch_locale_from_polish_to_english` (English) — both assert respective locale labels present | ✅ COVERED |
| I18N-05 | Date/time follows locale conventions | `assert_locale_rendered` checks `lang` attribute; calendar.html uses `Intl.DateTimeFormat` with `locale_bcp47` (pl-PL); Polish month names in rendered output | ✅ COVERED |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-20

---

## Validation Audit 2026-03-20

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

Reconstructed from phase artifacts (State B — no prior VALIDATION.md). All 3 requirements (I18N-01, I18N-04, I18N-05) have automated test coverage. 72 tests pass across relevant test files.
