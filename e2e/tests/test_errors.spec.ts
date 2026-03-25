import { test, expect } from '@playwright/test';

test.describe('Error Resilience', () => {

  test.describe('Auth Redirects — Unauthenticated', () => {
    test.use({ storageState: { cookies: [], origins: [] } });

    test('unauthenticated /dashboard redirects to login', async ({ page }) => {
      await page.goto('/dashboard');
      await page.waitForURL('**/auth/login**');
      await expect(page).toHaveURL(/\/auth\/login/);
    });

    test('unauthenticated /billing/settings redirects to login', async ({ page }) => {
      await page.goto('/billing/settings');
      // SessionValidationMiddleware catches missing cookies and redirects all
      // non-public routes to /auth/login with 302
      await page.waitForURL('**/auth/login**');
      await expect(page).toHaveURL(/\/auth\/login/);
    });
  });

  test.describe('API Error Responses — Unauthenticated', () => {
    test.use({ storageState: { cookies: [], origins: [] } });

    test('API without auth is rejected by middleware', async ({ page }) => {
      const response = await page.request.post('/api/billing/checkout', {
        headers: { 'Content-Type': 'application/json' },
        data: { plan: 'pro', billing_period: 'monthly' },
        maxRedirects: 0,
      });

      // SessionValidationMiddleware redirects unauthenticated requests to /auth/login
      expect(response.status()).toBe(302);
      expect(response.headers()['location']).toContain('/auth/login');
    });
  });

  test.describe('API Validation Errors — Authenticated', () => {
    test.use({ storageState: 'e2e/playwright/.auth/pro.json' });

    test('API with invalid plan returns 422 validation error', async ({ page }) => {
      const response = await page.request.post('/api/billing/checkout', {
        headers: { 'Content-Type': 'application/json' },
        data: { plan: 'invalid_plan', billing_period: 'monthly' },
      });

      expect(response.status()).toBe(422);
      const body = await response.json();
      expect(body.detail).toBeTruthy();
    });
  });

});
