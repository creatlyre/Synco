# Phase 46: Landing Page UX - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Improve landing page navigation and UX: add Features nav link, add mobile hamburger menu, add brand tagline to login page, add GitHub link to footer, and audit text contrast.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — UX improvement phase. Items:
- Add `#features` anchor link to landing nav (currently only Pricing and Sign in)
- Add mobile hamburger toggle — currently Pricing link has `hidden sm:inline`, so only Sign in shows on mobile
- Add brand tagline to login.html card (below `.brand` heading, before h1)
- Add GitHub link to footer (next to terms/privacy/refund links)
- Audit text contrast: check `text-gray-400` and `text-gray-500` against dark bg `#0f0a2e`

</decisions>

<code_context>
## Existing Code Insights

### Landing Nav (line 86-96)
```html
<nav class="sticky top-0 z-40 ...">
  <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
    <a href="/">Dobry Plan</a>
    <div class="flex items-center gap-4">
      <a href="/pricing" class="hidden sm:inline">Pricing</a>
      <a href="/auth/login">Sign in</a>
    </div>
  </div>
</nav>
```
- No #features link, no hamburger menu
- Pricing link hidden on mobile via `hidden sm:inline`

### Landing Footer (line 457-473)
- Terms, Privacy, Refund links
- "Made with" text
- Language switcher (PL | EN)
- No social links

### Login Page (login.html)
- Self-contained HTML (not extending base.html)
- Has `.brand` class with logo + app name
- Has `<h1>` with login title
- No brand tagline or subtitle

### Section IDs
- `id="features"` at line 236
- `id="pricing"` at line 390
- No `id` on hero or other sections

</code_context>

<specifics>
## Specific Ideas

None — UX improvement phase with clear scope from phase name.

</specifics>

<deferred>
## Deferred Ideas

None.
</deferred>
