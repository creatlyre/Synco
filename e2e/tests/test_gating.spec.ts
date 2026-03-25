import { test, expect } from '@playwright/test';

test.describe('Entitlement Gating — Free User Blocked', () => {
  test.use({ storageState: 'e2e/playwright/.auth/free.json' });

  test('free user gets 403 on /shopping', async ({ page }) => {
    const response = await page.goto('/shopping');
    expect(response?.status()).toBe(403);

    await expect(page.getByRole('link', { name: 'See Plans' })).toBeVisible();
    await expect(page.locator('h2')).not.toBeEmpty();
  });

  test('free user gets 403 on /budget/stats', async ({ page }) => {
    const response = await page.goto('/budget/stats');
    expect(response?.status()).toBe(403);

    await expect(page.getByRole('link', { name: 'See Plans' })).toBeVisible();
    await expect(page.locator('h2')).not.toBeEmpty();
  });

  test('free user gets 403 on /budget/import', async ({ page }) => {
    const response = await page.goto('/budget/import');
    expect(response?.status()).toBe(403);

    await expect(page.getByRole('link', { name: 'See Plans' })).toBeVisible();
    await expect(page.locator('h2')).not.toBeEmpty();
  });
});

test.describe('Entitlement Gating — API 403 Response', () => {
  test.use({ storageState: 'e2e/playwright/.auth/free.json' });

  test('API request to gated route returns 403 JSON with upgrade header', async ({ page }) => {
    // page.request sends without Accept: text/html, triggering the API 403 path
    const response = await page.request.get('/shopping');
    expect(response.status()).toBe(403);

    const body = await response.json();
    expect(body.detail).toBe('Upgrade required');

    const headers = response.headers();
    expect(headers['x-upgrade-url']).toBe('/billing/settings');
  });
});

test.describe('Entitlement Gating — Pro User Allowed', () => {
  test.use({ storageState: 'e2e/playwright/.auth/pro.json' });

  test('pro user loads /shopping with 200', async ({ page }) => {
    const response = await page.goto('/shopping');
    expect(response?.status()).toBe(200);
  });

  test('pro user loads /budget/stats without 403', async ({ page }) => {
    const response = await page.goto('/budget/stats');
    // Gating check: pro user must NOT get 403 (may get 500 if no budget data yet)
    expect(response?.status()).not.toBe(403);
  });

  test('pro user loads /budget/import with 200', async ({ page }) => {
    const response = await page.goto('/budget/import');
    expect(response?.status()).toBe(200);
  });
});
