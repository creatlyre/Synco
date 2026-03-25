import { test, expect } from '@playwright/test';

test.describe('Calendar', () => {
  test('month grid renders with day cells', async ({ page }) => {
    await page.goto('/calendar');

    // Wait for HTMX to load month grid content
    await page.locator('#month-grid').waitFor({ state: 'attached' });

    // Day cells are buttons with data-year attribute inside the grid
    const dayCells = page.locator('#month-grid button[data-year]');
    await expect(dayCells.first()).toBeVisible({ timeout: 15_000 });

    // Shortest month has 28 days, grid may include padding from adjacent months
    const cellCount = await dayCells.count();
    expect(cellCount).toBeGreaterThanOrEqual(28);
  });

  test('month navigation changes displayed month', async ({ page }) => {
    await page.goto('/calendar');

    // Wait for month grid to load
    const dayCells = page.locator('#month-grid button[data-year]');
    await expect(dayCells.first()).toBeVisible({ timeout: 15_000 });

    // Capture current month heading text
    const monthHeading = page.locator('#month-grid h3');
    const initialMonth = await monthHeading.textContent();

    // Click "next month" navigation button (contains → arrow)
    const nextBtn = page.locator('#month-grid button').filter({ hasText: '→' });
    await nextBtn.click();

    // Wait for HTMX to swap new content
    await page.waitForResponse(
      (resp) => resp.url().includes('/calendar/month') && resp.status() === 200,
    );

    // After swap, verify day cells are still present
    await expect(page.locator('#month-grid button[data-year]').first()).toBeVisible();

    // Month heading should have changed
    await expect(monthHeading).not.toHaveText(initialMonth!);
  });

  test('event entry button opens modal', async ({ page }) => {
    await page.goto('/calendar');

    // Wait for page to fully load
    await expect(
      page.locator('#month-grid button[data-year]').first(),
    ).toBeVisible({ timeout: 15_000 });

    // Click event entry button
    const eventBtn = page.locator('#event-entry-open-btn');
    await expect(eventBtn).toBeVisible();
    await eventBtn.click();

    // Modal should become visible (has role="dialog")
    const modal = page.locator('#event-entry-modal[role="dialog"]');
    await expect(modal).toBeVisible();

    // Close modal without submitting — click close button
    const closeBtn = page.locator('#event-entry-close-btn');
    if (await closeBtn.isVisible()) {
      await closeBtn.click();
    }
  });
});
