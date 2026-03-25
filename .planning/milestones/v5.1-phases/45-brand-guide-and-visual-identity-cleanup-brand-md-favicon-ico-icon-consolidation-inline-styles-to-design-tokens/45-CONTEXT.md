# Phase 45: Brand Guide & Visual Identity Cleanup - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Create BRAND.md documenting the visual identity (colors, fonts, logo usage, tone). Add favicon link to base.html. Extract repeated inline color values from landing.html into CSS custom properties.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — infrastructure/cleanup phase. Specific items:
- Create BRAND.md at project root documenting brand palette, typography, logo files, and tone
- Add favicon `<link>` to base.html `<head>` (landing.html has it, base.html doesn't)
- Define CSS custom properties for repeated color values in landing.html `<style>` block
- Replace static inline `style=` attributes with classes using those custom properties where feasible
- Skip Jinja2-dynamic inline styles ({{ color }}-based feature card styles)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `public/icons/logo.svg` — SVG logo (calendar+sync icon, indigo-to-violet gradient, 32x32 viewBox)
- `public/icons/icon-192.png`, `icon-512.png` — PNG raster icons
- `public/icons/icon-maskable-192.png`, `icon-maskable-512.png` — maskable PWA icons
- `public/icons/logo-app-512.png` — app store icon
- `public/images/logo-mark.webp` — small logo mark for nav
- `public/images/logo-wordmark.webp` — wordmark for OG image
- `public/manifest.json` — PWA manifest with theme_color `#1e1553`, background_color `#0f0a2e`

### Brand Colors (extracted from landing.html)
- Background: `#0f0a2e` (deep navy)
- Nav bg: `rgba(15,10,46,0.85)` (same hue, 85% opacity)
- Card gradient base: `rgba(26,20,68,0.5)` to `rgba(15,10,46,0.4)` (repeated 6+ times)
- Primary: `#6366f1` (indigo-500) / `rgba(99,102,241,...)`
- Accent: `#8b5cf6` (violet-500) / `rgba(139,92,246,...)`
- CTA gradient: `#6366f1` → `#8b5cf6`
- CTA hover: `#818cf8` → `#a78bfa`
- Success accent: `#34d399` (emerald)
- Text gradient: `#c7d2fe` → `#a5b4fc` → `#818cf8` → `#c084fc`

### Typography
- Display: "Plus Jakarta Sans" (wght 500-800)
- Body: "DM Sans" (wght 400-600, italic)

### Inline Style Patterns
- 27 inline `style=` attributes in landing.html
- ~10 use Jinja2 `{{ color }}` template vars (dynamic, can't extract)
- ~17 use static repeated values (candidates for CSS custom properties)
- Common repeats: body bg, nav bg, card gradient, glow orbs, letter-spacing

### Missing
- No `<link rel="icon">` in base.html (only in landing.html)
- No favicon.ico file
- No BRAND.md or style guide documentation

</code_context>

<specifics>
## Specific Ideas

None — infrastructure phase with clear scope from phase name.

</specifics>

<deferred>
## Deferred Ideas

None.
</deferred>
