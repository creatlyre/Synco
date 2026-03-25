import { test, expect } from '@playwright/test';

test.describe('Sync Status — Not Connected State', () => {
  test.use({ storageState: 'e2e/playwright/.auth/pro.json' });

  test('sync status API returns not connected for test account', async ({ page }) => {
    const response = await page.request.get('/api/sync/status');
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.google_connected).toBe(false);
  });

  test('calendar page shows sync status section', async ({ page }) => {
    const response = await page.goto('/calendar');
    expect(response?.status()).toBe(200);

    await expect(page.locator('#sync-status')).toBeVisible();
  });
});
