---
phase: 33
slug: go-to-market
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-24
---

# Phase 33 — Validation Strategy

> Per-phase validation contract for Go-to-Market (pricing page, landing page, legal pages, checkout flow, CI/CD, launch checklist).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (Python 3.12) |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest tests/test_go_to_market.py -v --tb=short` |
| **Full suite command** | `python -m pytest tests/test_go_to_market.py tests/test_billing.py -v` |
| **Estimated runtime** | ~0.3 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_go_to_market.py -v --tb=short`
- **After every plan wave:** Run `python -m pytest tests/ -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 33-01-01 | 01 | 1 | GTM-01 | integration | `pytest tests/test_go_to_market.py::TestPricingPage -v` | ✅ | ✅ green |
| 33-01-01 | 01 | 1 | GTM-03 | integration | `pytest tests/test_go_to_market.py::TestSelfHostedCheckout -v` | ✅ | ✅ green |
| 33-01-02 | 01 | 1 | GTM-01 | integration | `pytest tests/test_go_to_market.py::TestPricingPage -v` | ✅ | ✅ green |
| 33-02-01 | 02 | 1 | GTM-02 | integration | `pytest tests/test_go_to_market.py::TestLandingPage -v` | ✅ | ✅ green |
| 33-02-02 | 02 | 1 | GTM-04 | integration | `pytest tests/test_go_to_market.py::TestLegalPages -v` | ✅ | ✅ green |
| 33-03-01 | 03 | 1 | GTM-05 | artifact | `pytest tests/test_go_to_market.py::TestDockerArtifacts -v` | ✅ | ✅ green |
| 33-03-02 | 03 | 1 | GTM-05 | artifact | `pytest tests/test_go_to_market.py::TestLaunchChecklist -v` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.*

- [x] `tests/test_go_to_market.py` — 28 tests covering GTM-01 through GTM-05
- [x] `tests/conftest.py` — shared fixtures (test_client, authenticated_client, test_db)

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Requirement Coverage Summary

| Requirement | Description | Tests | Status |
|---|---|---|---|
| GTM-01 | Pricing page with SaaS tiers + self-hosted | `TestPricingPage` (4 tests) | ✅ COVERED |
| GTM-02 | Landing page with CTA | `TestLandingPage` (4 tests) | ✅ COVERED |
| GTM-03 | Checkout for recurring + one-time | `TestSelfHostedCheckout` (3 tests) + existing `TestBillingSchemas` | ✅ COVERED |
| GTM-04 | Legal pages published | `TestLegalPages` (8 tests) | ✅ COVERED |
| GTM-05 | Launch checklist + CI/CD artifacts | `TestLaunchChecklist` (5 tests) + `TestDockerArtifacts` (4 tests) | ✅ COVERED |

---

## Validation Audit 2026-03-24

| Metric | Count |
|--------|-------|
| Gaps found | 5 |
| Resolved | 5 |
| Escalated | 0 |

---

## Validation Sign-Off

- [x] All tasks have automated verify commands
- [x] Sampling continuity: no consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 1s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-24
