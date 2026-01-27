import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {

    test('Successful Registration', async ({ page }) => {
        // Navigate to registration page
        await page.goto('/register');

        // Verify page title/header
        await expect(page.locator('h3:has-text("Create an account")')).toBeVisible();

        // Fill out the form
        await page.selectOption('#role', 'farmer');
        await page.fill('#firstName', 'Test');
        await page.fill('#lastName', 'User');
        await page.fill('#email', `test-${Date.now()}@example.com`);
        await page.fill('#phone', '9876543210');
        await page.fill('#dob', '1990-01-01');
        await page.fill('#address', '123 Test Lane');
        await page.fill('#upiId', 'test@upi');
        await page.fill('#password', 'Password123!');
        await page.fill('#confirmPassword', 'Password123!');

        // Handle the success alert
        page.once('dialog', async dialog => {
            expect(dialog.message()).toContain('Registration successful');
            await dialog.accept();
        });

        // Submit form
        await page.click('button[type="submit"]');
    });

    test('Password Mismatch Validation', async ({ page }) => {
        await page.goto('/register');

        await page.fill('#firstName', 'Test');
        await page.fill('#lastName', 'User');
        await page.fill('#email', 'mismatch@example.com');
        await page.fill('#phone', '9876543210');
        await page.fill('#dob', '1990-01-01');
        await page.fill('#address', '123 Test Lane');
        await page.fill('#upiId', 'test@upi');
        await page.fill('#password', 'Password123!');
        await page.fill('#confirmPassword', 'DifferentPassword');

        await page.click('button[type="submit"]');

        // Expect error message
        await expect(page.locator('text=Passwords do not match')).toBeVisible();
    });

});
