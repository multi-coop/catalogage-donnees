
import AxeBuilder from '@axe-core/playwright';
import { test, expect } from '@playwright/test';


test.describe('homepage', () => { // 2
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/'); // 3
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    //@ts-ignore this is a hot fix untild this isssue will be resolved https://github.com/dequelabs/axe-core-npm/issues/601
    const accessibilityScanResults = await new AxeBuilder.default({ page }).analyze(); // 4

    expect(accessibilityScanResults.violations).toEqual([]); // 5
  });
});
