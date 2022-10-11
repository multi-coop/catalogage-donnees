import { expect } from "@playwright/test";
import { test } from "./fixtures.js";

test.describe("Static pages", () => {
  test("Visits the 'Mentions légales' page", async ({ page }) => {
    await page.goto("/");
    await page.click("text=Mentions légales");

    await expect(
      page.locator("role=heading[level=1] >> text=Mentions légales")
    ).toBeVisible();
  });
});
