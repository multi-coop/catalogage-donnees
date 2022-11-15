

import { test, expect } from '@playwright/test';


test.describe('homepage', () => { // 2
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/'); // 3

    // try {
      //  const axeBuilder = new  AxeBuilder({page})

      //  const results = await axeBuilder.analyze();

      //  console.log(results);
     
    //   } catch (e) {
    //      console.log(e)
    //   }
  });
});
