# Phase 38: Gated Features & Entitlements E2E — Research

**Researched:** 2026-03-25
**Domain:** Playwright E2E tests for plan-gated features and page rendering

## Standard Stack

- **Playwright** (from Phase 36 infrastructure) — TypeScript test specs
- **3 Playwright projects:** `free`, `pro`, `family-plus` with pre-authenticated storage states
- **Target:** Live Railway deployment via `E2E_BASE_URL`

## Key Playwright Patterns for This Phase

### 1. Checking HTTP Status on page.goto()

`page.goto()` returns a `Response` object. It does NOT throw for valid HTTP status codes (including 403). Status is retrieved via `response.status()`:

```typescript
const response = await page.goto('/shopping');
expect(response?.status()).toBe(403);
```

This is the primary pattern for gating tests — navigate as free user, assert 403.

### 2. API-Level Testing with request Context

`page.request` provides an `APIRequestContext` that carries browser cookies automatically:

```typescript
const response = await page.request.get('/shopping/items');
expect(response.status()).toBe(403);
const body = await response.json();
expect(body.detail).toBe('Upgrade required');
const upgradeUrl = response.headers()['x-upgrade-url'];
expect(upgradeUrl).toBe('/billing/settings');
```

This lets us test API gating without browser navigation — validates the JSON error response and custom header.

### 3. Content Assertions on 403 Pages

Even though `page.goto()` returns 403, Playwright still renders the page content. We can assert on DOM elements:

```typescript
const response = await page.goto('/shopping');
expect(response?.status()).toBe(403);
// Page still renders upgrade_required.html
await expect(page.locator('a[href="/pricing"]')).toBeVisible();
```

### 4. Page Render Verification (200 OK)

For authorized users, standard pattern:

```typescript
const response = await page.goto('/budget/overview');
expect(response?.status()).toBe(200);
await expect(page.locator('h1, h2, [class*="heading"]')).toBeVisible();
```

## Architecture Insights

### Upgrade Page Structure (from `upgrade_required.html`)

The upgrade page is a full template extending `base.html`. Key verifiable elements:
- **Feature-specific headline:** `upgrade.{feature}_headline` i18n key (rendered as `<h2>`)
- **Feature-specific icon:** Different SVG per feature (shopping, budget_stats, budget_import)
- **CTA "See plans" link:** `<a href="/pricing">` — NOT `/billing/settings` as in API header
- **"Go back" button:** `onclick="history.back()"`
- **Locked label:** SVG lock icon with `upgrade.locked_label` text
- **Benefits section:** 4 feature-specific benefits

### Gating Mechanism

```
require_plan("pro", "family_plus")
├── HTML request (Accept: text/html) → UpgradeRedirect(feature) → upgrade_required.html (403)
└── API request (no text/html) → HTTPException(403, "Upgrade required", X-Upgrade-URL: /billing/settings)
```

Feature names from `_PATH_FEATURE_MAP`:
| Path | Feature |
|------|---------|
| `/shopping` | `shopping` |
| `/budget/stats` | `budget_stats` |
| `/budget/import` | `budget_import` |

### Pages by Access Level

| Page | Access | Gated? |
|------|--------|--------|
| `/budget/overview` | All authenticated | No |
| `/budget/expenses` | All authenticated | No |
| `/budget/income` | All authenticated | No |
| `/budget/settings` | All authenticated | No |
| `/budget/stats` | Pro, Family+ | Yes |
| `/budget/import` | Pro, Family+ | Yes |
| `/shopping` | Pro, Family+ | Yes |

### Sync Status API

`GET /api/sync/status` returns JSON:
```json
{
  "status": "google_not_connected",
  "google_connected": false,
  "oauth_configured": true/false,
  "household_size": N,
  "calendar_last_sync": null
}
```
Test accounts have no Google OAuth → `google_connected: false`, `status` contains `not_connected`.

## Don't Hand-Roll

- Auth login — already handled by Phase 36 storage state fixtures
- Server startup — tests hit live Railway deployment
- Cleanup logic — all tests are read-only

## Common Pitfalls

1. **Asserting redirect instead of 403** — The app returns a rendered 403 page, NOT a 302 redirect. Tests must check `response.status() === 403`.
2. **CTA link confusion** — The HTML upgrade page links to `/pricing`, but the API header uses `/billing/settings`. Tests should check what's actually in the template.
3. **Sync status values** — The status string may be `google_not_connected` or `oauth_not_configured` depending on server config. Test for `google_connected: false` which is always reliable for test accounts.

## Validation Architecture

### Test Framework
- Playwright Test (TypeScript) — same as Phase 36/37
- Config: `playwright.config.ts` (created in Phase 36)
- Run: `npx playwright test tests/e2e/test_gating.spec.ts tests/e2e/test_budget.spec.ts tests/e2e/test_shopping.spec.ts tests/e2e/test_sync.spec.ts`

### Verification Strategy
Each test file is self-verifying — Playwright assertions fail the test on mismatch. No separate unit tests needed.

### Requirement → Test Mapping

| REQ ID | Test File | Test Name | What's Verified |
|--------|-----------|-----------|-----------------|
| GATE-E2E-01 | test_gating.spec.ts | free user blocked from /shopping | 403 status + upgrade page |
| GATE-E2E-02 | test_gating.spec.ts | free user blocked from /budget/stats | 403 status + upgrade page |
| GATE-E2E-03 | test_gating.spec.ts | free user blocked from /budget/import | 403 status + upgrade page |
| GATE-E2E-04 | test_gating.spec.ts | API 403 with JSON body and header | JSON detail + X-Upgrade-URL |
| SHOP-E2E-01 | test_shopping.spec.ts | pro user loads shopping page | 200 status + content visible |
| SHOP-E2E-02 | test_shopping.spec.ts | shopping list container renders | Key DOM elements present |
| BUD-E2E-01 | test_budget.spec.ts | budget overview renders | 200 + heading visible |
| BUD-E2E-02 | test_budget.spec.ts | budget expenses/income render | 200 + content containers |
| BUD-E2E-03 | test_budget.spec.ts | budget stats renders for pro | 200 + stats content visible |
| SYNC-E2E-01 | test_sync.spec.ts | sync status API returns not connected | JSON google_connected: false |
| SYNC-E2E-02 | test_sync.spec.ts | calendar page shows sync status | UI element with status text |
