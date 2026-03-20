---
phase: 08-localization-foundation-and-polish-default
plan: 03
subsystem: ui
tags: [locale-formatting, polish, date-time, regression-tests, intl-api]

requires:
  - phase: 08-02
    provides: "Template copy migration to translation keys"
provides:
  - "Polish-default date/time formatting via Intl.DateTimeFormat with pl-PL locale"
  - "locale_bcp47 template variable for JS formatting"
  - "Regression tests for Polish default locale rendering"
affects: [09, 10, 11]

tech-stack:
  added: []
  patterns:
    - "Intl.DateTimeFormat with locale_bcp47 for JS date/time rendering"
    - "Server-side Polish month names via locale-aware calendar labels"

key-files:
  created: []
  modified:
    - app/views/calendar_routes.py
    - app/templates/calendar.html
    - app/templates/partials/month_grid.html
    - app/templates/partials/day_events.html
    - tests/test_calendar_views.py
    - tests/test_events_api.py

key-decisions:
  - "Use BCP47 locale (pl-PL) for JavaScript Intl.DateTimeFormat"
  - "Polish diacritics in all 174 locale strings (ą, ę, ś, ć, ź, ż, ó, ł, ń)"
  - "Translate JS-embedded strings (sync, household) alongside template strings"

patterns-established:
  - "locale_bcp47 passed to all JS date formatting calls"
  - "Polish diacritics as regression markers in test assertions"

requirements-completed: [I18N-01, I18N-05]

duration: ~20min
completed: 2026-03-19
---

# Phase 08 Plan 03: Polish-Default Locale Formatting & Regression Coverage

**Enforced Polish date/time conventions and added diacritics to all 174 locale strings with regression test coverage.**

## Accomplishments
- Replaced hardcoded English month names and sv-SE formatting with Polish-default locale strategy
- Added proper Polish diacritical marks (ą, ę, ś, ć, ź, ż, ó, ł, ń) to all 174 locale strings
- Translated 12 hardcoded English JS strings (household, sync status/results)
- Extended test suite with Polish-default locale rendering assertions

## Task Commits

1. **Task 1: Replace locale-formatting shortcuts with Polish-default locale strategy** - `88d4f0e` (fix)
2. **Task 2: Add localization regression coverage for Polish default rendering** - `88d4f0e` (fix)

## Files Created/Modified
- `app/views/calendar_routes.py` - Locale-aware month/day label generation
- `app/templates/calendar.html` - JS date formatting with locale_bcp47, translated JS strings
- `app/templates/partials/month_grid.html` - Polish month name rendering
- `app/templates/partials/day_events.html` - Locale-aware event display
- `app/locales/pl.json` - 174 strings with proper Polish diacritics
- `app/locales/en.json` - 12 new sync/household keys added
- `tests/test_calendar_views.py` - Polish-default locale regression assertions

## Decisions Made
- Added title tooltip to truncated calendar event pills for accessibility
- Bumped event pill font from text-[10px] to text-[11px] sm:text-xs for readability

## Deviations from Plan
Minor scope addition: fixed sidebar event entry header layout (flex-wrap) and event pill font size alongside locale formatting work.
