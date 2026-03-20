---
phase: 08-localization-foundation-and-polish-default
plan: 01
subsystem: i18n
tags: [i18n, localization, polish, jinja2, fastapi]

requires:
  - phase: 07
    provides: "Stable calendar UI and API surface to localize"
provides:
  - "resolve_locale() with Polish default and query/cookie/accept-language cascade"
  - "translate() with interpolation and English fallback"
  - "get_translator() closure for Jinja templates"
  - "inject_template_i18n() context helper for TemplateResponse"
  - "set_locale_cookie_if_param() for cookie persistence"
  - "Polish (pl.json) and English (en.json) locale dictionaries"
affects: [08-02-PLAN, 08-03-PLAN, 09, 10]

tech-stack:
  added: []
  patterns:
    - "LRU-cached JSON locale loading"
    - "Jinja globals injection via inject_template_i18n"
    - "Cookie + query param + Accept-Language locale cascade"

key-files:
  created:
    - app/i18n.py
    - app/locales/pl.json
    - app/locales/en.json
  modified:
    - main.py
    - app/views/calendar_routes.py

key-decisions:
  - "Polish (pl) as DEFAULT_LOCALE, not English"
  - "Cookie-based persistence with 365-day expiry and lax sameSite"
  - "LRU cache (maxsize=8) for locale dictionary loading"
  - "BCP47 mapping (pl→pl-PL, en→en-US) for JS Intl API"

patterns-established:
  - "inject_template_i18n: single injection point for locale + translator into all template contexts"
  - "normalize_locale: defensive parsing handles None, empty, hyphenated, underscored input"

requirements-completed: [I18N-01, I18N-04]

duration: ~30min
completed: 2026-03-19
---

# Phase 08 Plan 01: i18n Contracts & Polish-Default Wiring

**Created localization runtime with Polish default, bilingual dictionaries (174 keys each), and Jinja template injection.**

## Accomplishments
- Created `app/i18n.py` with locale resolution cascade (query → cookie → Accept-Language → Polish default)
- Built Polish and English locale dictionaries with 174 translation keys covering auth, calendar, modals, sync, invite, and common UI copy
- Wired `inject_template_i18n()` into main.py TemplateResponse middleware for automatic `t()`, `locale`, and `locale_bcp47` in all templates
- Added `set_locale_cookie_if_param()` for persistent locale via `?lang=xx` query parameter

## Task Commits

1. **Task 1: Create localization contracts and bilingual resource files** - `2a4dd7c` (feat)
2. **Task 2: Wire i18n context into template rendering with Polish default** - `2a4dd7c` (feat)

## Files Created/Modified
- `app/i18n.py` - Locale resolution, translation lookup, Jinja context injection
- `app/locales/pl.json` - Polish translation dictionary (174 keys)
- `app/locales/en.json` - English translation dictionary (174 keys)
- `main.py` - inject_template_i18n and set_locale_cookie_if_param wiring
- `app/views/calendar_routes.py` - Locale context passed to template responses

## Decisions Made
- Polish as default locale (not English) — matches primary user base
- Single `inject_template_i18n()` injection point rather than per-route locale setup
- BCP47 locale mapping for JavaScript Intl API compatibility

## Deviations from Plan
None - plan executed as written. Both tasks landed in a single atomic commit.
