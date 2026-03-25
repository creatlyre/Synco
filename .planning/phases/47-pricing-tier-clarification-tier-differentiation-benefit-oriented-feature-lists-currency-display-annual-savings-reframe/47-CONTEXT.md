# Phase 47: Pricing Tier Clarification - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Clarify pricing tiers on both landing page and pricing page: rewrite feature lists as benefit-oriented copy, i18n the hardcoded "zł" currency, and show annual savings on the landing page pricing preview.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — copy/UX phase. Items:
- Rewrite `pricing.free_f1`–`f4`, `pricing.pro_f1`–`f5`, `pricing.family_f1`–`f4` in en.json and pl.json with benefit-framing (outcome, not feature name)
- Replace hardcoded "zł" with i18n key (`pricing.currency`) in landing.html and pricing.html
- Add annual pricing display to landing page pricing preview (show monthly and annual with savings badge)
- Add `pricing.pro_desc` and `pricing.family_desc` improvements to better differentiate tiers

</decisions>

<code_context>
## Existing Code Insights

### Pricing Feature Keys (en.json)
```
pricing.free_f1: "Shared calendar"
pricing.free_f2: "Basic budget tracking"
pricing.free_f3: "1 custom category per type"
pricing.free_f4: "Basic shopping list"
pricing.pro_f1: "Unlimited categories"
pricing.pro_f2: "Expense charts & analytics"
pricing.pro_f3: "NLP event parsing"
pricing.pro_f4: "OCR receipt scanning"
pricing.pro_f5: "Email notifications"
pricing.family_f1: "Everything in Pro"
pricing.family_f2: "Extended storage"
pricing.family_f3: "All premium features"
pricing.family_f4: "Priority email support"
```

### Hardcoded Currency
- landing.html line 402: `0 <span class="text-sm font-normal text-gray-400">zł</span>`
- landing.html line 415: `19 <span class="text-sm font-normal text-gray-400">zł{{ t('pricing.per_month') }}</span>`
- landing.html line 432: `29 <span class="text-sm font-normal text-gray-400">zł{{ t('pricing.per_month') }}</span>`
- pricing.html line 40: `0 <span class="text-base font-normal text-gray-400">zł</span>`
- pricing.html line 63: `zł{{ t('pricing.per_month') }}`
- pricing.html line 104: `zł{{ t('pricing.per_month') }}`
- pricing.html line 154: `199 <span class="text-base font-normal text-gray-400">zł</span>`

### Pricing Page (pricing.html)
- Extends base.html
- Has billing period toggle (monthly/annual)
- Has Pro price `id="pro-price"` and Family price `id="family-price"` (JS swaps values)
- Has feature comparison table with all tiers
- Self-hosted card with one-time 199 zł price

### Annual Pricing (config.py)
- `STRIPE_PRO_ANNUAL_PRICE_ID` and `STRIPE_FAMILY_PLUS_ANNUAL_PRICE_ID` exist
- Pricing page has billing toggle, but landing preview only shows monthly

</code_context>

<specifics>
## Specific Ideas

None — copy/UX clarification phase.

</specifics>

<deferred>
## Deferred Ideas

None.
</deferred>
