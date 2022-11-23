import { expect } from "@playwright/test";
import { test } from "./fixtures.js";

test.describe("Static pages", () => {
  test("Visits the 'Mentions légales' page", async ({ page }) => {
    await page.goto("/");
    await page.click("text=Mentions légales");

    await expect(page).toHaveTitle("Mentions légales - catalogue.data.gouv.fr");
    await expect(
      page.locator("role=heading[level=1] >> text=Mentions légales")
    ).toBeVisible();
  });

  test("Visits the 'Vie privée' page", async ({ page }) => {
    await page.goto("/");
    await page.click("text=Vie privée");

    await expect(page).toHaveTitle("Vie privée - catalogue.data.gouv.fr");
    await expect(
      page.locator("role=heading[level=1] >> text=Vie privée")
    ).toBeVisible();
  });

  test("Visits the 'Declaration d'accessibilité' page", async ({ page }) => {
    await page.goto("/");
    await page.click("text=Accessibilité: non conforme");

    await expect(page).toHaveTitle(
      "Déclaration accessibilité  - catalogue.data.gouv.fr"
    );
  });

  test("Visits the '404' page", async ({ page }) => {
    await page.goto("/tata");
    await expect(
      page.locator("role=heading[level=1] >> text=Page non trouvée")
    ).toBeVisible();
  });
});
