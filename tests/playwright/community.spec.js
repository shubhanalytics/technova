const { test, expect } = require('@playwright/test');

test.describe('Community page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:9000/community.html');
  });

  test('shows coming soon banner', async ({ page }) => {
    await expect(page.locator('.community-coming')).toBeVisible();
    await expect(page.locator('.community-coming h3')).toHaveText('Community opening soon');
  });

  test('discussion UI hidden', async ({ page }) => {
    await expect(page.locator('#newDiscussion')).toBeHidden();
    await expect(page.locator('#discussionsList')).toBeHidden();
  });

  test('hamburger toggles nav', async ({ page }) => {
    // emulate narrow viewport so the hamburger is visible
    await page.setViewportSize({ width: 375, height: 800 });
    const toggle = page.locator('#navToggle');
    await expect(toggle).toBeVisible();
    await toggle.click();
    const nav = page.locator('#main-nav');
    await expect(nav).toBeVisible();
    await expect(nav).toHaveClass(/open/);
  });

  test('no horizontal overflow', async ({ page }) => {
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    expect(overflow).toBeFalsy();
  });
});
