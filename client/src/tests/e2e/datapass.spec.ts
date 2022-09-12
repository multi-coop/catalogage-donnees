import { TEST_EMAIL, TEST_ORGANIZATION } from "./constants.js";
import { test } from "./fixtures.js";
import { expect } from "@playwright/test";

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

    await page
      .locator("text=Votre compte peut être associé à plusieurs organisations.")
      .waitFor();
    await page.locator("text=Ministère de la culture").check();

    const button = await page.locator("text=Associer mon compte");

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
