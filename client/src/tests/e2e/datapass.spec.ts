import { test } from "./fixtures.js";
import { expect } from "@playwright/test";
import { TEST_EMAIL, TEST_ORGANIZATION } from "./constants.js";

test.describe("Datapass", () => {
  test("A user tried to log in but no organization has been found", async ({
    page,
  }) => {
    await page.goto("/auth/datapass/create-organization");
    await expect(page).toHaveTitle(
      "Connexion avec MonComptePro : aucune organisation enregistrée - catalogue.data.gouv.fr"
    );

    await page
      .locator(
        "text=Votre compte n’est associé à aucune organisation enregistrée..."
      )
      .waitFor();
  });

  test("A user can log in with datapass", async ({ page, apiToken }) => {
    const info = {
      email: TEST_EMAIL,
      organization_siret: TEST_ORGANIZATION.siret,
      api_token: apiToken,
      role: "USER",
    };
    await page.goto(
      `/auth/datapass/login?user_info=${encodeURIComponent(
        JSON.stringify(info)
      )}`
    );

    await page.locator("text='Recherchez un jeu de données'").waitFor();

    // The user's organization was saved as the current organization.
    await page.click("text='Contribuer'");
    await page.locator("text=Ministère de la Culture").waitFor();
  });

  test("A user picks the organization they want to be linked with", async ({
    page,
  }) => {
    const token = "<fake>";
    const info = {
      email: TEST_EMAIL,
      organizations: [TEST_ORGANIZATION],
    };
    await page.goto(
      `/auth/datapass/pick-organization?token=${token}&info=${encodeURIComponent(
        JSON.stringify(info)
      )}`
    );
    await expect(page).toHaveTitle(
      "Connexion avec MonComptePro : choisir une organisation - catalogue.data.gouv.fr"
    );

    await page
      .locator("text=Votre compte peut être associé à plusieurs organisations.")
      .waitFor();
    await page.locator("text=Ministère de la culture").check();

    const button = page.locator("text=Associer mon compte");

    const [request, response] = await Promise.all([
      page.waitForRequest("**/auth/datapass/users/"),
      page.waitForResponse("**/auth/datapass/users/"),
      button.click(),
    ]);

    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(403);

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
      organizations: null, // Simulate backend sending invalid info
    };
    await page.goto(
      `/auth/datapass/pick-organization?token=${token}&info=${encodeURIComponent(
        JSON.stringify(info)
      )}`
    );

    await page
      .locator("text=Nous n'arrivons pas à retrouver vos informations ...")
      .waitFor();
  });
});
