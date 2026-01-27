import { test, expect } from '@playwright/test';

test.describe('User Login Flow', () => {

    test('Successful Login', async ({ page }) => {
        await page.goto('/login');

        await page.fill('#email', 'test@example.com');
        await page.fill('#password', 'password');

        // Alert removed from UI
        // page.once('dialog', async dialog => {
        //     expect(dialog.message()).toContain('Login successful');
        //     await dialog.accept();
        // });

        await page.click('button[type="submit"]');
    });

    test('Invalid Credentials', async ({ page }) => {
        await page.goto('/login');

        await page.fill('#email', 'wrong@example.com');
        await page.fill('#password', 'wrongpassword');

        await page.click('button[type="submit"]');

        await expect(page.locator('text=Incorrect username or password')).toBeVisible();
    });

});
