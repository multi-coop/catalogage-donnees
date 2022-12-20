import { test } from "./fixtures.js";
import { expect } from "@playwright/test";

test.describe("acesssibility", () => {
  test("home page should not have any automatically detectable accessibility issues", async ({
    page,
    makeAxeBuilder,
  }) => {
    await page.goto("/");

    const accessibilityScanResults = await makeAxeBuilder().analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("accessibility declaration page should not have any automatically detectable accessibility issues", async ({
    page,
    makeAxeBuilder,
  }) => {
    await page.goto("/declaration-daccessibilite");

    const accessibilityScanResults = await makeAxeBuilder().analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("'mentions légales' page should not have any automatically detectable accessibility issues", async ({
    page,
    makeAxeBuilder,
  }) => {
    await page.goto("/mentions-legales");

    const accessibilityScanResults = await makeAxeBuilder().analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
