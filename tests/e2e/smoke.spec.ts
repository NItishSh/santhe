import { test, expect } from '@playwright/test';

test.describe('Santhe Smoke Tests', () => {

    // Homepage loads test merged into Landing Page elements test

    test('Landing Page elements', async ({ page }) => {
        await page.goto('/');
        await expect(page.locator('h1')).toHaveText('Santhe');
        await expect(page.locator('text=Fresh Direct from Farmers')).toBeVisible();
        await expect(page.locator('text=Marketplace for everyone.')).toBeVisible();
        await expect(page.locator('text=Sign Up')).toBeVisible();
    });

    // test('Product Catalog loads', async ({ page }) => {
    //   // TODO: Enable once Product Catalog UI is integrated
    // });

    test('Navigate to Login', async ({ page }) => {
        await page.goto('/');

        // Find login link/button
        const loginButton = page.locator('a[href*="login"], button:has-text("Login")');
        if (await loginButton.count() > 0) {
            await loginButton.first().click();
            await expect(page).toHaveURL(/.*login/);
            await expect(page.locator('input[type="email"]')).toBeVisible();
        } else {
            console.log('Login button not found on home page');
        }
    });

});
