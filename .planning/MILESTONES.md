# Milestones

## v3.0 Overview Detail & Performance (Shipped: 2026-03-20)

**Phases completed:** 2 phases (16-17), 4 plans

**Key accomplishments:**

- Accordion month detail in year overview — click any month row to expand inline one-time expense breakdown with full CRUD (add, edit, delete)
- Replaced Tailwind CDN play script (~300KB runtime) with prebuilt static CSS (34KB minified)
- Added httpx connection pooling in SupabaseStore (shared singleton client)
- FastAPI StaticFiles mount for serving CSS with caching headers
- 6 new integration tests for month detail CRUD
- 222 tests passing across all subsystems

**Stats:**

- 11 files changed
- 598 insertions, 298 deletions
- Timeline: 2026-03-20 (1 day)
- 10 commits

**Git range:** v2.0 -> v3.0

## v1.1 Localization and Language Switching (Shipped: 2026-03-20)

**Phases completed:** 4 phases, 10 plans, 0 tasks

**Key accomplishments:**

- Built i18n foundation with `resolve_locale()`, `translate()`, and Jinja template integration — Polish as default locale across all views.
- Added language switcher UI (Polish/English) with cookie and localStorage persistence.
- Enabled locale-aware NLP and OCR parsing with Polish keyword dictionaries and bilingual fallback.
- Implemented day-click quick-entry for rapid event creation with auto-calculated end-time (+1h).
- Added multi-reminder support to Event model with Google Calendar sync payload generation.
- Comprehensive test coverage: 145 tests passing across auth, events, views, NLP, sync, and integration.

**Stats:**

- 60 files changed
- 5,014 insertions, 479 deletions
- Timeline: 2026-03-19 to 2026-03-20 (2 days)
- 47 commits

**Git range:** ebe4787 -> 4026efa

**Known gaps:**

- Phases 08, 09, 10 missing formal VERIFICATION.md files (process gaps only — all tests green)
- Phase 9 SUMMARY frontmatter `requirements_completed` empty (should list I18N-02, I18N-03, I18N-06)
- Reminder UI not exposed in quick-entry form (backend supports it, deferred to v2 REM-02)

---

## v1.0 milestone (Shipped: 2026-03-19)

**Delivered:** Household shared-calendar MVP with Google auth, event CRUD/recurrence, Google sync, NLP/OCR quick-add, and final UI/UX polish.

**Phases completed:** 7 phases, 22 plans, 39 tasks

**Key accomplishments:**

- Implemented two-user household invitation and shared calendar access flow.
- Delivered authenticated event CRUD with month/day calendar views and interactive UI updates.
- Added RFC5545 recurrence support with DST-safe handling.
- Added Google Calendar export and automatic sync hooks for event create/update/delete.
- Added quick-add natural language parsing, ambiguity-year confirmation, and OCR image extraction with review/fallback.
- Completed UI/UX hardening: invite back navigation, modal entry workflow, keyboard/focus behavior, and mobile responsiveness with regression coverage.

**Stats:**

- 129 files changed
- 17,380 insertions, 2 deletions
- Timeline: 2026-03-18 to 2026-03-19

**Git range:** 3e8eed6bfb14cef7a352b93ba4d70f62b907e235 -> 2368f2d0c519236484961f9c6e74769289c58ba4

**Known gaps:**

- Milestone audit is present and passed for phases 1-6; phase 7 was completed afterward without a separate final audit pass.

---
