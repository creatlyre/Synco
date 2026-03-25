import { test, expect } from '@playwright/test';

test.describe('Shopping Page — Pro User Render', () => {
  test.use({ storageState: 'e2e/playwright/.auth/pro.json' });

  test('shopping page loads with list container', async ({ page }) => {
    const response = await page.goto('/shopping');
    expect(response?.status()).toBe(200);

    // Verify the real shopping page rendered (not the upgrade page)
    await expect(page.locator('#main-content')).toBeVisible();
    await expect(page.locator('a[href="/pricing"]')).not.toBeVisible();
  });
});
