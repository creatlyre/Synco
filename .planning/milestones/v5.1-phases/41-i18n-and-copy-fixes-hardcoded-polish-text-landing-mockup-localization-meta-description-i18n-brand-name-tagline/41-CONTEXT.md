# Phase 41: i18n & Copy Fixes - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix all hardcoded Polish text and non-i18n strings across templates. Move them to locale JSON files so both PL and EN work correctly. Add brand tagline as an i18n key.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — infrastructure/code cleanup phase. Specific items to address:
- Hardcoded meta description in base.html line 6 → use `{{ t() }}`
- Hardcoded "Install Dobry Plan for quick access" in PWA banner (base.html) → add locale key
- Hardcoded Polish taglines in landing.html lines 104-105 → add locale keys
- Hardcoded Polish mockup data in landing.html (Mleko, Chleb, Masło, 2340 zł) → add locale keys
- Hardcoded "Dobry Plan" brand name in landing mockup → use `{{ t('app.name') }}`
- Brand tagline definition as locale key for both PL and EN

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/i18n.py` — locale resolution, `t()` helper, JSON-based locale files
- `app/locales/pl.json` and `app/locales/en.json` — ~680+ keys each
- `{{ t('key') }}` pattern used consistently across all templates
- `{{ t('app.name') }}` already used in most page titles and navbar

### Established Patterns
- All user-facing strings use `t('section.key')` in Jinja2 templates
- Locale keys follow dot notation: `section.subsection_name`
- Landing page keys prefixed with `landing.*`
- Mockup-specific keys already exist: `landing.mock_budget`, `landing.mock_shopping`, `landing.mock_next`, `landing.mock_event`

### Integration Points
- `app/templates/base.html` — meta description, PWA install banner
- `app/templates/landing.html` — hero taglines, mockup sidebar data
- `app/locales/pl.json` and `app/locales/en.json` — new keys added here

</code_context>

<specifics>
## Specific Ideas

No specific requirements — infrastructure phase with clear scope from phase name.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>
