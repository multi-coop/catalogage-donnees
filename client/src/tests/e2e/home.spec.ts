import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants.js";
import { test } from "./fixtures.js";

test.describe("Landing Page", () => {
  test("Visits the home page without being logged in", async ({ page }) => {
    await page.goto("/");

    await page
      .locator(
        "text=Bienvenue sur le service de catalogage de données de l’État"
      )
      .waitFor();
    await page.locator("text=Comment accéder aux catalogues ?").waitFor();
  });
});

test.describe("Catalog list", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the home page", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Catalogue");

    await page.locator("data-test-id=dataset-list-item").first().click();

    await page.locator("text='Modifier'").waitFor();
  });

  test("Sees the pagination", async ({ page }) => {
    await page.goto("/");

    // Page size is 50 items, only 1 page during E2E tests.
    const currentPage = page.locator(
      "[data-testid='pagination-list'] [aria-current='page']"
    );
    await expect(page.locator("text=Première page")).toBeDisabled();
    await expect(page.locator("text=Page précédente")).toBeDisabled();
    await expect(currentPage).toHaveText("1");
    await expect(page.locator("text=Page suivante")).toBeDisabled();
    await expect(page.locator("text=Dernière page")).toBeDisabled();
  });
});
