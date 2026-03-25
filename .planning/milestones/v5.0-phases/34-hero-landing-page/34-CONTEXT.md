# Phase 34: Hero Landing Page - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning
**Source:** Discussion — all areas deferred to Claude's discretion

<domain>
## Phase Boundary

Enhance the existing landing page at `/` (built in Phase 33) into a higher-converting marketing page. Adds social proof section, Open Graph/Twitter Card meta tags, improved hero with dual CTAs (register + sign in), and full Polish/English i18n coverage for all new content. Tests validate new sections.

**NOT in scope:** New pages, navigation changes, pricing logic changes, checkout flow changes, new routes.

</domain>

<decisions>
## Implementation Decisions

### Social Proof Strategy
- Use **trust indicators** instead of fabricated testimonials (no real users yet)
- Three trust badges: open-source (AGPL), GDPR-compliant, PWA installable
- Add a "Zaufało nam X gospodarstw domowych" / "Trusted by X households" counter placeholder (start at a modest number or "Dołącz do rosnącej społeczności" / "Join our growing community")
- Keep it honest — no fake testimonials, no inflated numbers

### Hero Visual Enhancement
- Keep the existing CSS-only calendar mockup (it's distinctive and loads fast)
- Polish the mockup: add subtle event labels visible inside colored day cells to make it feel more real
- Ensure the dual CTA is prominent: primary "Zacznij za darmo" → `/auth/register`, secondary "Zaloguj się" → `/auth/login`
- Current hero CTA goes to `/auth/login` — change primary to `/auth/register` for conversion focus

### OG & SEO Meta Tags
- Add Open Graph tags: `og:title`, `og:description`, `og:image`, `og:url`, `og:type=website`
- Add Twitter Card tags: `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`
- OG image: use a static placeholder path `/static/icons/og-image.png` (can be created later, just set the meta tag)
- Meta description already exists — enhance with conversion-focused wording

### Claude's Discretion
- Exact wording for trust badges and social proof section
- Animation timing/easing refinements
- Specific OG description copy
- Whether to add a subtle background pattern or keep current gradient

</decisions>

<specifics>
## Specific Ideas

- Phase 33 CONTEXT.md specified "no social proof for v1 launch" — Phase 34 explicitly adds it
- Landing page tone: warm, personal, practical (from Phase 33 decisions)
- Primary audience: Polish couples/households
- Bilingual PL/EN via existing i18n cookie system
- Current landing page is 208 lines of Jinja2 with inline CSS — keep same pattern

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Landing Page
- `app/templates/landing.html` — Current landing page template (208 lines, all sections)
- `app/locales/pl.json` — Polish translations (lines 554-584 for landing.* keys)
- `app/locales/en.json` — English translations (matching landing.* keys)

### Route & i18n
- `main.py` — Root route handler (line 181-188), `inject_template_i18n` pattern
- `app/i18n.py` — Translation function `t()` and locale resolution

### Tests
- `tests/test_go_to_market.py` — Existing landing page tests (lines 50-70)

### Prior Context
- `.planning/phases/33-go-to-market/33-CONTEXT.md` — Phase 33 landing page decisions (carried forward)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `landing.html` template with hero, features, how-it-works, pricing, footer sections
- CSS-only calendar mockup in hero section
- `inject_template_i18n()` for template context with `t()` function
- `style.css` with Tailwind utilities and glass-morphism patterns

### Established Patterns
- All user-facing text via `t('landing.key')` i18n function
- Inline `<style>` block for landing-specific CSS (animations, hero-glow)
- Dark theme: `#0f0a2e` bg, `rgba(26,20,68,0.4)` card bg, indigo-500 accents
- Font stack: Plus Jakarta Sans (display), DM Sans (body)

### Integration Points
- New i18n keys added to both `pl.json` and `en.json`
- New tests added to `tests/test_go_to_market.py` (existing test class)
- No new routes needed — all changes within existing landing.html template

</code_context>

<deferred>
## Deferred Ideas

- A/B testing different hero copy (future growth phase)
- Real user testimonials (collect after launch)
- Video demo in hero section
- Animated feature showcase

</deferred>

---

*Phase: 34-hero-landing-page*
*Context gathered: 2026-03-24 via discussion (Claude's discretion)*
