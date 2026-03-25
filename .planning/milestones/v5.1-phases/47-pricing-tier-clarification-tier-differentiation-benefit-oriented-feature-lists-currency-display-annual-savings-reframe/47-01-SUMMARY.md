# Phase 47 — Plan 01 Summary: Pricing Tier Clarification

## What Was Done

### Task 1: Benefit-Oriented Copy & Currency i18n
- Added `pricing.currency` i18n key: EN "PLN", PL "zł"
- Rewrote 13 pricing feature keys in both locales with benefit/outcome framing:
  - Free: "Shared calendar" → "Shared family calendar — see everyone's schedule", "Basic budget tracking" → "Track monthly income & expenses", etc.
  - Pro: "NLP event parsing" → "Add events in natural language", "OCR receipt scanning" → "Scan receipts with OCR", etc.
  - Family: "Everything in Pro" → "Everything in Pro, plus:", "Extended storage" → "Extended data storage", etc.
- Replaced 4 hardcoded `zł` in pricing.html with `{{ t('pricing.currency') }}`
- Replaced 3 hardcoded `zł` in landing.html pricing with `{{ t('pricing.currency') }}`
- Added `lp-pro-price` and `lp-family-price` IDs to landing price spans

### Task 2: Annual Pricing Toggle on Landing
- Added 3 new i18n keys: `landing.pricing_monthly`, `landing.pricing_annual`, `landing.pricing_save`
- Added billing toggle UI between pricing subtitle and card grid (switch button with role="switch", aria-checked, aria-label)
- Added script at page bottom: toggles annual/monthly, swaps Pro 19→15 and Family 29→24, shows/hides "Save ~17%" badge
- Labels switch colors (white/gray-400) on toggle

## Files Modified
- `app/locales/en.json` — pricing.currency key + 13 benefit-oriented feature rewrites + 3 toggle keys
- `app/locales/pl.json` — same (Polish translations)
- `app/templates/pricing.html` — 4 hardcoded zł → i18n
- `app/templates/landing.html` — 3 hardcoded zł → i18n, price IDs, toggle UI + script

## Verification
- 0 hardcoded `>zł<` or `>zł{` in templates
- Toggle, price IDs confirmed present
- 581 tests passed, 12 skipped

## Commit
- `db165c2` feat(47-01): benefit-oriented pricing copy, currency i18n, annual toggle on landing
