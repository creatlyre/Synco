# Phase 46 — Plan 01 Summary: Landing Page UX Improvements

## What Was Done

### Task 1: Nav, Footer, Contrast
- Added Features nav link (`#features`) before Pricing in desktop nav
- Added mobile hamburger menu (`<button>` + `<div id="mobile-menu">`) with Features, Pricing, Sign in links — visible below `sm:` breakpoint, toggles via `classList.toggle('hidden')` with `aria-expanded` updates
- Desktop Sign in button now hidden on mobile (`hidden sm:inline-flex`) to avoid duplication with hamburger menu
- Added GitHub link in footer (using existing repo URL from founder section)
- Added i18n keys: `landing.nav_features` (EN: Features, PL: Funkcje), `footer.github` (EN/PL: GitHub)
- Contrast audit: replaced all 11 `text-gray-500` instances with `text-gray-400` (~5.5:1 ratio vs ~3.3:1 on #0f0a2e background)

### Task 2: Login Tagline
- Added `auth.tagline` i18n key: EN "Your household, finally in sync", PL "Twój dom, wreszcie ogarnięty"
- Added `.tagline` CSS class in login.html style block
- Inserted `<p class="tagline">{{ t('auth.tagline') }}</p>` between brand div and h1

## Files Modified
- `app/templates/landing.html` — nav restructure, hamburger menu, footer GitHub link, contrast fixes
- `app/templates/login.html` — tagline CSS + HTML
- `app/locales/en.json` — 3 new keys (nav_features, auth.tagline, footer.github)
- `app/locales/pl.json` — 3 new keys (matching Polish translations)

## Verification
- Mobile menu present (`mobile-menu` ID), Features link (`#features`), GitHub link in footer
- Login tagline present, locale keys exist
- 581 tests passed, 12 skipped

## Commit
- `d577f77` feat(46-01): nav Features link, mobile hamburger menu, footer GitHub, login tagline, contrast fixes
