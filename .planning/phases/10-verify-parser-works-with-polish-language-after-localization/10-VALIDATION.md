---
phase: 10
slug: verify-parser-works-with-polish-language-after-localization
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-19
audited: 2026-03-20
---

# Phase 10 - Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | pyproject.toml |
| Quick run command | `.venv\\Scripts\\python.exe -m pytest tests/test_nlp.py tests/test_events_api.py -q` |
| Full suite command | `.venv\\Scripts\\python.exe -m pytest tests/ -q` |
| Estimated runtime | ~4 seconds |

## Sampling Rate

- After every task commit: run quick parser/OCR suite
- After final plan wave: run full suite
- Before verify-work: full suite green
- Max feedback latency: 60 seconds

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | I18N-07 | unit+api | `.venv\\Scripts\\python.exe -m pytest tests/test_nlp.py -q` | yes | COVERED |
| 10-01-02 | 01 | 1 | I18N-07 | api | `.venv\\Scripts\\python.exe -m pytest tests/test_events_api.py -k "parse or ocr" -q` | yes | COVERED |
| 10-02-01 | 02 | 2 | I18N-07 | unit+api | `.venv\\Scripts\\python.exe -m pytest tests/test_nlp.py tests/test_events_api.py -q` | yes | COVERED |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

## Manual-Only Verifications

All phase behaviors have automated verification.

## Validation Sign-Off

- [x] All tasks have automated verify commands
- [x] Sampling continuity maintained
- [x] No watch-mode flags
- [x] Feedback latency target defined
- [x] nyquist_compliant true

Approval: validated 2026-03-20

## Validation Audit 2026-03-20

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

**Tests verified:** 62 passed (42 NLP + 20 events API), 0 failures.
**Requirement I18N-07:** Fully covered by 14 Polish NLP tests + 3 OCR locale tests + regression gate.
