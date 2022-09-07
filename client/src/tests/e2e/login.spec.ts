import { expect } from "@playwright/test";
import { TEST_EMAIL, TEST_PASSWORD } from "./constants.js";
import { test } from "./fixtures.js";

test.describe("Login", () => {
  test("Redirects unauthenticated visits to login page", async ({ page }) => {
    await page.goto("/fiches/search");
    await page
      .locator(
        "text='Bienvenue sur le service de catalogage de données de l’État'"
      )
      .waitFor();
    await expect(page).toHaveURL("/");
  });

  test("Logs in", async ({ page }) => {
    await page.goto("/login");

    await expect(page).toHaveTitle("Connexion");

    const email = page.locator("form [name=email]");
    await email.fill(TEST_EMAIL);
    expect(await email.inputValue()).toBe(TEST_EMAIL);

    const password = page.locator("form [name=password]");
    await password.fill(TEST_PASSWORD);
    expect(await password.inputValue()).toBe(TEST_PASSWORD);

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest("**/auth/login/"),
      page.waitForResponse("**/auth/login/"),
      button.click(),
    ]);

    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(200);
    const json = await response.json();
    expect(json.email).toBe(TEST_EMAIL);
    expect(json).toHaveProperty("api_token");

    await page.locator("text='Recherchez un jeu de données'").waitFor();
    await expect(page).toHaveURL("/");
  });

  test("Fails to log in due to bad password", async ({ page }) => {
    await page.goto("/login");

    const email = page.locator("form [name=email]");
    await email.fill(TEST_EMAIL);
    expect(await email.inputValue()).toBe(TEST_EMAIL);

    const password = page.locator("form [name=password][type=password]");
    await password.fill("wrongpassword");
    expect(await password.inputValue()).toBe("wrongpassword");

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest("**/auth/login/"),
      page.waitForResponse("**/auth/login/"),
      button.click(),
    ]);
    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(401);

    // Still on login page
    await expect(page).toHaveURL("/login");

    const exampleProtectedPage = "/contribuer";
    await page.goto(exampleProtectedPage);
    await page.waitForURL("/");
  });
});
