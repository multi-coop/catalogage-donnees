import { test } from "./fixtures.js";
import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants.js";

test.describe("accessibilty - pages without required authentication", () => {
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

test.describe("accessibilty - pages with required authentication", () => {
  test.use({ storageState: STATE_AUTHENTICATED });
  test("home page (connected state) should not have any automatically detectable accessibility issues", async ({
    page,
    makeAxeBuilder,
  }) => {
    await page.goto("/");

    const accessibilityScanResults = await makeAxeBuilder().analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test.use({ storageState: STATE_AUTHENTICATED });
  test("search page should not have any automatically detectable accessibility issues", async ({
    page,
    makeAxeBuilder,
  }) => {
    await page.goto("/fiches/search");

    const accessibilityScanResults = await makeAxeBuilder().analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
