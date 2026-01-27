import { test, expect } from '@playwright/test';

test.describe('User Profile', () => {

    test('Loads profile with correct user data', async ({ page }) => {
        // 1. Register a new user to ensure we have a clean state
        const uniqueId = Date.now();
        const email = `profile-${uniqueId}@example.com`;
        const password = 'Password123';
        const fullName = 'Profile Test User';

        await page.goto('/register');
        await page.selectOption('#role', 'farmer');
        await page.fill('#firstName', 'Profile');
        await page.fill('#lastName', 'TestUser');
        await page.fill('#email', email);
        await page.fill('#phone', '9876543210');
        await page.fill('#dob', '1990-01-01');
        await page.fill('#address', '123 Address');
        await page.fill('#upiId', 'profile@upi');
        await page.fill('#password', password);
        await page.fill('#confirmPassword', password);
        await page.click('button[type="submit"]');

        // Wait for redirect to login page
        await page.waitForURL(/\/login/);

        // Perform Login
        await page.fill('#email', email);
        await page.fill('#password', password);
        await page.click('button[type="submit"]'); // Button says "Sign in" but type="submit" works
        await page.waitForURL('/');

        // 2. Open User Menu
        // Backend doesn't support full_name yet, so it uses username which is email prefix in register page logic
        const expectedUsername = email.split('@')[0];

        await expect(page.locator(`button:has-text("${expectedUsername}")`)).toBeVisible({ timeout: 10000 });
        await page.click(`button:has-text("${expectedUsername}")`);

        // 3. Click Profile
        await expect(page.locator('text=Profile')).toBeVisible();
        await page.click('text=Profile');
        await expect(page).toHaveURL('/profile');

        // 4. Verify Content
        await expect(page.locator('h1:has-text("My Profile")')).toBeVisible();
        await expect(page.locator(`text=${expectedUsername}`)).toBeVisible();
        await expect(page.locator(`text=${email}`)).toBeVisible();
        await expect(page.locator('text=farmer')).toBeVisible();

        // 5. Logout from Profile
        await page.click('button:has-text("Log Out")');
        await expect(page).toHaveURL('/login');
    });

    test('Redirects to login if not authenticated', async ({ page }) => {
        await page.goto('/profile');
        await expect(page).toHaveURL(/.*login/);
    });

});
