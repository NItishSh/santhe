import { test, expect } from '@playwright/test';

test.describe('Authentication State UI', () => {

    test('Shows Logout button after login and reverts on logout', async ({ page }) => {


        // 1. Initial State
        await page.goto('/');
        await expect(page.locator('text=Log In')).toBeVisible();
        await expect(page.locator('text=Sign Up')).toBeVisible();
        await expect(page.locator('text=Log Out')).toBeHidden();

        const password = 'Password123';

        // 2. Register
        await page.goto('/register');
        await page.selectOption('#role', 'farmer');
        await page.fill('#firstName', 'Auth');
        await page.fill('#lastName', 'TestUser');
        const email = `authtest-${Date.now()}@example.com`;
        await page.fill('#email', email);
        await page.fill('#phone', '9876543210');
        await page.fill('#dob', '1990-01-01');
        await page.fill('#address', '123 Auth Lane');
        await page.fill('#upiId', 'auth@upi');
        await page.fill('#password', password);
        await page.fill('#confirmPassword', password);
        await page.click('button[type="submit"]');

        // Wait for registration alert handling
        await page.waitForTimeout(2000);

        // 3. Login
        await page.goto('/login');
        await page.waitForLoadState('networkidle');
        await page.fill('#email', email);
        await page.fill('#password', password);
        await page.click('button[type="submit"]');

        await page.waitForTimeout(5000);

        // Debug: Wait for either success or failure
        try {
            await Promise.race([
                expect(page).toHaveURL('/', { timeout: 10000 }),
                expect(page.locator('.text-red-500')).toBeVisible({ timeout: 10000 })
            ]);
        } catch (e) {
            console.log("Neither redirect nor error appeared within timeout.");
        }

        // Capture error if visible
        const errorMsg = page.locator('.text-red-500');
        if (await errorMsg.isVisible()) {
            console.error(`Login Error Displayed: ${await errorMsg.textContent()}`);
        }

        // 4. Verify Logged In State
        // Check if token exists in localStorage
        const token = await page.evaluate(() => localStorage.getItem('token'));
        if (token) {
            console.log("Token found in localStorage");
        } else {
            console.error("No token found in localStorage");
        }
        expect(token).toBeTruthy();

        // Verify User Menu is present
        // Verify User Menu is present
        // UserMenu now shows First Name + Last Name
        const expectedName = "Auth TestUser";
        await expect(page.locator(`button:has-text("${expectedName}")`)).toBeVisible({ timeout: 10000 });

        // Open User Menu
        await page.click(`button:has-text("${expectedName}")`);

        // Verify Menu Items
        await expect(page.locator('text=Profile')).toBeVisible();
        await expect(page.locator('text=My Orders')).toBeVisible();
        await expect(page.locator('text=Log Out')).toBeVisible();

        // 5. Perform Logout
        await page.click('text=Log Out');

        // 6. Verify Logged Out State
        await expect(page.locator('text=Log In')).toBeVisible();
        // User menu button should be hidden
        await expect(page.locator(`button:has-text("${expectedName}")`)).toBeHidden();
    });

});
