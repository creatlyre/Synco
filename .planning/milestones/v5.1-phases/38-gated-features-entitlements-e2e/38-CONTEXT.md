# Phase 38: Gated Features & Entitlements E2E - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Plan-gated features enforce correct access control and render properly for authorized users. This phase writes E2E test specs verifying entitlement gating (free → upgrade redirect, pro → full access) and page rendering for budget, shopping, and sync features. Uses Phase 36's Playwright infrastructure and follows Phase 37's read-only test pattern.

</domain>

<decisions>
## Implementation Decisions

### Upgrade Redirect Verification (Gating Tests)
- When a **free** user hits a gated page (`/shopping`, `/budget/stats`, `/budget/import`), the app returns `upgrade_required.html` with **403 status**
- Tests MUST verify:
  1. The response status is 403 (not a 302 redirect — it's a rendered template)
  2. The page displays the correct **feature name** for the blocked route (shopping, budget_stats, budget_import — from `_PATH_FEATURE_MAP`)
  3. The page contains a **working upgrade link** pointing to `/billing/settings`
- Use the `free` Playwright project for all gating tests
- API-level gating: non-HTML requests to gated endpoints return 403 JSON `{"detail": "Upgrade required"}` with `X-Upgrade-URL: /billing/settings` header — test at least one API endpoint

### Budget Page Render Verification
- Budget overview (`/budget/overview`), expenses (`/budget/expenses`), and income (`/budget/income`) are accessible to **all authenticated users** (no plan gating)
- Use `pro` project for render tests (has data; avoids any edge cases with free tier)
- Verify each page loads with 200 status and contains a key identifying element (page heading or main content container)
- **Read-only** — no form submissions, no data mutations (consistent with Phase 37 pattern)
- Budget settings (`/budget/settings`) page: verify it loads with settings form visible

### Shopping Page Render Verification (Pro Access)
- `/shopping` is gated to pro/family_plus — use `pro` project
- Verify page loads with 200, shopping list container renders
- No item creation or deletion — read-only verification only

### Sync "Not Connected" State Verification
- Google Sync status appears on the `/calendar` page (already partially tested in Phase 37)
- Additionally test the `/api/sync/status` JSON endpoint directly:
  - Returns `google_not_connected` status for test accounts (no Google OAuth association)
  - Returns `google_connected: false` in response
- Use `pro` project (sync is available to all plans but needs an authenticated user)

### Test Data Strategy
- Consistent with Phase 37: **all tests are read-only / non-destructive**
- No shopping items created, no budget entries modified, no expenses added
- Gating tests only navigate to pages and verify the response — no form interaction

### Test File Organization
- `tests/e2e/test_gating.spec.ts` — All entitlement gating tests (free user blocked, upgrade page content, API 403)
- `tests/e2e/test_budget.spec.ts` — Budget page rendering (overview, expenses, income, settings, stats)
- `tests/e2e/test_shopping.spec.ts` — Shopping page rendering for authorized users
- `tests/e2e/test_sync.spec.ts` — Sync status API and UI state verification
- Each file uses the appropriate Playwright project (free for gating, pro for feature access)

### Claude's Discretion
- Exact selectors for identifying page headings and content containers
- Whether to combine sync API test with the calendar sync UI test from Phase 37 or keep separate
- Number of gated routes to test (at minimum: `/shopping`, `/budget/stats`, `/budget/import`)
- Whether budget settings page test belongs in this phase or is redundant with Phase 37

</decisions>

<specifics>
## Specific Ideas

- The `upgrade_required.html` template receives a `feature` context variable — tests should assert the page text includes the feature name or a human-readable version of it
- The upgrade link on the blocked page points to `/billing/settings` — verify it's an actual clickable link (not just text)
- For API gating test, use `fetch` or Playwright's `request` context to hit a gated API endpoint (e.g., `/shopping/items`) with free user auth and verify 403 + JSON body + `X-Upgrade-URL` header
- Pro user should be able to visit all gated pages without any redirect or 403

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 36 & 37 (dependencies)
- `.planning/phases/36-e2e-test-infrastructure/36-CONTEXT.md` — Playwright setup, projects, auth strategy
- `.planning/phases/37-core-app-e2e-tests/37-CONTEXT.md` — Read-only test pattern, test file organization

### Entitlement gating
- `app/billing/dependencies.py` — `require_plan()`, `UpgradeRedirect`, `_PATH_FEATURE_MAP`, `get_current_plan()`
- `main.py` lines 153-166 — `_upgrade_redirect_handler` renders `upgrade_required.html` with 403 status
- `app/templates/upgrade_required.html` — Upgrade page template (feature name, upgrade link)

### Gated views
- `app/shopping/views.py` — `/shopping` gated to `pro, family_plus`
- `app/budget/overview_views.py` — `/budget/stats` and `/budget/import` gated to `pro, family_plus`; `/budget/overview` ungated

### Ungated budget views
- `app/budget/expense_views.py` — `/budget/expenses` (all authenticated users)
- `app/budget/income_views.py` — `/budget/income` (all authenticated users)
- `app/budget/views.py` — `/budget/settings` (all authenticated users)

### Sync
- `app/sync/routes.py` — `GET /api/sync/status` returns `google_not_connected` for unlinked accounts
- `app/templates/calendar.html` — Sync status UI section with `#sync-status` element

### Shopping
- `app/shopping/routes.py` — `/shopping/items`, `/shopping/sections` API endpoints (gated via view dependency)
- `app/templates/shopping.html` — Shopping list page template

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 36 Playwright projects: `free`, `pro`, `family-plus` with pre-authenticated storage states
- Phase 37 test patterns: read-only verification, `page.goto()` + status check + element visibility

### Gating Mechanism Detail
- `require_plan("pro", "family_plus")` is a FastAPI dependency injected on route handlers
- For HTML requests (`Accept: text/html`): raises `UpgradeRedirect(feature)` → caught by exception handler → renders `upgrade_required.html` with 403
- For API requests: returns `HTTPException(403)` with `{"detail": "Upgrade required"}` and `X-Upgrade-URL` header
- Feature names derived from path: `/shopping` → `"shopping"`, `/budget/stats` → `"budget_stats"`, `/budget/import` → `"budget_import"`

### Established Patterns
- Server-rendered Jinja2 + HTMX — E2E tests interact with real HTML
- `get_user_plan_for_template(user, db)` injects `user_plan` into template context (used for conditional UI)
- Budget pages use common layout pattern: heading + content area with tables/forms

### Integration Points
- Free user storage state → navigate to gated page → verify 403 + upgrade template
- Pro user storage state → navigate to same gated page → verify 200 + real content
- Sync status endpoint returns JSON with `status`, `google_connected`, `oauth_configured` fields

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 38-gated-features-entitlements-e2e*
