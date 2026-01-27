import { test, expect } from '@playwright/test';

test.describe('Product Catalog Integration', () => {

    test('Home page loads and displays products (or empty state)', async ({ page }) => {
        await page.goto('/');

        // Verify Title
        await expect(page.locator('h1:has-text("Santhe")')).toBeVisible();

        // Verify either product grid or empty state
        // We expect "Empty state" initially if DB is empty, or cards if seeded.
        // The previous implementation shows "Loading fresh produce..." then the grid or empty.

        // Wait for loading to finish
        await expect(page.locator('text=Loading fresh produce...')).toBeHidden({ timeout: 10000 });

        const grid = page.locator('.grid');
        const emptyState = page.locator('text=No products found');

        if (await grid.count() > 0) {
            await expect(grid).toBeVisible();
            console.log('Product grid found');
        } else {
            await expect(emptyState).toBeVisible();
            console.log('Empty state found');
        }
    });

});
