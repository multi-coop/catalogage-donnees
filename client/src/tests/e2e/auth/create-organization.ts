import { test } from "../fixtures";
test.describe("Landing Page", () => {
  test("Visits the home page without being logged in", async ({ page }) => {
    await page.goto("/auth/datapass/create-organization");

    await page
      .locator(
        "text=Votre compte n’est associé à aucune organisation enregistrée..."
      )
      .waitFor();
  });
});
