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

  test("A user can NOT pick the organization he wants to be linked with -- bad token case", async ({
    page,
  }) => {
    const token = "not-valid";
    const info = {
      email: TEST_EMAIL,
      organizations: [
        {
          name: ORGANIZATION_NAME,
          siret: ORGANIZATION_SIRET,
        },
      ],
    };
    await page.goto(
      `/auth/datapass/pick-organization?token=${token}&info=${encodeURIComponent(
        JSON.stringify(info)
      )}`
    );

    await page
      .locator("text=Votre compte peut être associé à plusieurs organisations.")
      .waitFor();
    await page.locator("text=Ministère de la culture").check();
    await page.locator("text=Associer mon compte").click();

    await page
      .locator("text=Nous n'arrivons pas à créer votre compte.")
      .waitFor();
  });

  test("A user can NOT pick the organization he wants to be linked with -- no organizations found", async ({
    page,
  }) => {
    const token = "not-valid";
    const info = {
      email: TEST_EMAIL,
      organizations: null,
    };
    await page.goto(
      `/auth/datapass/pick-organization?token=${token}&info=${encodeURIComponent(
        JSON.stringify(info)
      )}`
    );

    await page
      .locator("text=Nous n'arrivons pas à retrouver vous informations ...")
      .waitFor();
  });
});
