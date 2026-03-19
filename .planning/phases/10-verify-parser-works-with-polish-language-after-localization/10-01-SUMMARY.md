---
phase: 10-verify-parser-works-with-polish-language-after-localization
plan: 01
subsystem: nlp
tags: [i18n, nlp, ocr, polish, locale, dateparser, easyocr]

requires:
  - phase: 09-language-switcher-persistence-and-translation-coverage
    provides: resolve_locale(), i18n infrastructure, locale cookie handling

provides:
  - Locale-aware NLPService.parse() with Polish keyword dictionaries
  - Locale-aware OCRService.parse_image() with Polish EasyOCR language support
  - Locale propagation from parse/OCR routes into service layer
  - Unicode-safe title extraction preserving Polish diacritics
  - Bilingual keyword fallback (always checks both locale + English)

affects: [10-02, parser tests, OCR tests]

tech-stack:
  added: []
  patterns:
    - "Locale-keyed class dictionaries for multilingual keyword matching"
    - "Merged dict fallback: {**en, **locale} for bilingual parsing"
    - "Unicode-safe title regex: [^\\w\\s] + [\\d_] instead of [^A-Za-z\\s]"

key-files:
  created: []
  modified:
    - app/events/nlp.py
    - app/events/ocr.py
    - app/events/routes.py
    - tests/test_events_api.py

key-decisions:
  - "Always merge English + locale keywords for bilingual fallback (users may type English with Polish UI)"
  - "Polish 'o HH' time pattern added for locale=pl (e.g., 'o 14' → 14:00)"
  - "dateparser receives both locale languages when locale != en"
  - "OCR reader initialized with [pl, en] when locale is pl"
  - "Both diacritical and ASCII-stripped forms accepted for Polish keywords"

patterns-established:
  - "Bilingual merge: {**DICT['en'], **DICT[locale]} ensures English always works as fallback"
  - "_normalize_locale() strips region/variant suffixes for consistent locale handling"

requirements-completed:
  - I18N-07

duration: 15min
completed: 2026-03-19
---

# Phase 10: Plan 01 Summary

**Locale-aware NLP/OCR parsing with Polish keyword dictionaries and Unicode-safe title extraction**

## Performance

- **Duration:** 15 min
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Added Polish keyword dictionaries for relative dates, weekdays, months, recurrence, and time defaults
- Replaced ASCII-only title regex with Unicode-safe character class preserving Polish diacritics
- Propagated locale from request context through parse and OCR endpoints into parser internals
- Implemented bilingual keyword fallback so English text parses correctly regardless of UI locale

## Task Commits

1. **Task 1+2: Locale-aware NLP/OCR parsing** - `b8e86c6` (feat)

## Files Created/Modified
- `app/events/nlp.py` - Added locale-keyed dictionaries, locale parameter, Polish keywords, Unicode-safe title regex
- `app/events/ocr.py` - Added locale parameter, Polish EasyOCR language support
- `app/events/routes.py` - Pass user_locale to parse() and parse_image()
- `tests/test_events_api.py` - Fixed OCR monkeypatch to accept locale keyword

## Decisions Made
- Merged English + locale keywords (bilingual fallback) to handle users typing English with Polish UI
- Added Polish "o HH" time pattern (e.g., "o 14" → 14:00) for locale=pl
- Both diacritical (ą, ć, ę) and ASCII-stripped (a, c, e) forms accepted for Polish keywords

## Deviations from Plan
- Combined Task 1 and Task 2 into single commit since they're tightly coupled
- Added bilingual keyword fallback (not in plan) to fix regression where default "pl" locale broke English text parsing

## Issues Encountered
- Default locale "pl" (from Phase 8) caused English test text to fail parsing — resolved by merging both locale dictionaries

## Next Phase Readiness
- Polish parsing infrastructure ready for test coverage in Plan 10-02
- All 28 NLP + 22 API tests pass with no regressions

---
*Phase: 10-verify-parser-works-with-polish-language-after-localization*
*Completed: 2026-03-19*
