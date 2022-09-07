import { TEST_EMAIL } from "./constants.js";
import { test } from "./fixtures.js";

test.describe("Datapass", () => {
  test("A user tried to log in but no organization has been found", async ({
    page,
  }) => {
    await page.goto("/auth/datapass/create-organization");

    await page
      .locator(
        "text=Votre compte n’est associé à aucune organisation enregistrée..."
      )
      .waitFor();
  });

  test("A user can log in with datapass", async ({ page, apiToken }) => {
    await page.goto(
      `/auth/datapass/login?role=USER&api_token=${apiToken}&email=${TEST_EMAIL}`
    );

    await page.locator("text='Recherchez un jeu de données'").waitFor();
  });
});
