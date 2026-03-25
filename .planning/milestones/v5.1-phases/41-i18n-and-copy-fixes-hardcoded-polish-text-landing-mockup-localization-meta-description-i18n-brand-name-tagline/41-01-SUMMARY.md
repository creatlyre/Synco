# Phase 41 Plan 01 Summary

**Status:** Complete
**Commit:** 9ca88f2

## What was done
- Added 10 new i18n keys to both `en.json` and `pl.json`: `app.meta_desc`, `app.tagline`, `pwa.install_prompt`, `pwa.install_btn`, `landing.tagline_shopping`, `landing.tagline_calendar`, `landing.mock_item_milk`, `landing.mock_item_bread`, `landing.mock_item_butter`, `landing.mock_balance`
- Replaced hardcoded meta description in `base.html` with `{{ t('app.meta_desc') }}`
- Replaced hardcoded PWA install banner text with `{{ t('pwa.install_prompt') }}` and `{{ t('pwa.install_btn') }}`
- Replaced hardcoded Polish taglines in `landing.html` with `{{ t('app.name') }}` + locale-aware text
- Replaced hardcoded Polish mockup items (Mleko, Chleb, Masło) and currency (2,340 zł) with locale keys

## Files modified
- `app/locales/en.json` — 10 new keys
- `app/locales/pl.json` — 10 new keys
- `app/templates/base.html` — meta description + PWA banner i18n
- `app/templates/landing.html` — taglines + mockup content i18n

## Verification
- All 10 locale keys present in both locale files
- 581 tests passing, 0 regressions
