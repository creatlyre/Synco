# Phase 42: Landing Page Copy & Messaging Overhaul - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Improve landing page copy across hero badge, CTAs, trust section, pricing descriptions, feature outcome framing, and brand narrative. All changes are to locale key values in en.json/pl.json — structure stays the same.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All copy decisions at Claude's discretion — improve messaging to be more benefit-oriented and compelling. The existing structure (sections, template layout) stays unchanged. Focus on:
- Hero badge: more compelling than "Free to start • Open Source"
- CTAs: stronger action verbs, urgency without pressure
- Trust copy: more specific social proof language
- Pricing descriptions: outcome-focused tier descriptions
- Feature copy: rewrite descriptions to lead with outcomes, not features
- Brand narrative consistency across all sections

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- All landing copy uses locale keys via `{{ t('landing.*') }}` and `{{ t('pricing.*') }}`
- Feature descriptions use title + desc + 3 bullet pattern
- Pricing uses title + price + note + 3 features per tier

### Established Patterns
- Tone: Casual, direct, second-person ("you", "your")
- PL tone: Warm, colloquial ("ogarnięty", "bliskich")
- Key action words: "Start", "Join", "Get organized"

### Integration Points
- `app/locales/en.json` and `app/locales/pl.json` — update existing key values only

</code_context>

<specifics>
## Specific Ideas

No specific requirements — copy improvement phase.

</specifics>

<deferred>
## Deferred Ideas

None.

</deferred>
