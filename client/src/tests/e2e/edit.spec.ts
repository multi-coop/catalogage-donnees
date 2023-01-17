import { expect } from "@playwright/test";
import {
  STATE_AUTHENTICATED,
  STATE_AUTHENTICATED_ADMIN,
  STATE_AUTHENTICATED_ADMIN_SANTE,
  STATE_AUTHENTICATED_SANTE,
} from "./constants.js";
import { test } from "./fixtures.js";

const DELETE_DATASET_BUTTON_LOCATOR = "text=Supprimer ce jeu de données";

test.describe("Edit dataset", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the edit page", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);
    await expect(page).toHaveTitle(
      "Modifier la fiche de jeu de données - catalogue.data.gouv.fr"
    );

    await page.locator("text=Ministère de la Culture").waitFor();

    // Check initial data

    const title = page.locator("form [name=title]");
    expect(await title.inputValue()).toBe(dataset.title);

    const description = page.locator("form [name=description]");
    expect(await description.inputValue()).toBe(dataset.description);

    expect(dataset.extraFieldValues).toHaveLength(1);
    const extraReferentiel = page.locator("form [name=referentiel]");
    expect(await extraReferentiel.inputValue()).toBe(
      dataset.extraFieldValues[0].value
    );

    // Make and submit changes

    const newTitleText = "Other title";
    expect(newTitleText).not.toBe(dataset.title);
    await title.fill(newTitleText);
    expect(await title.inputValue()).toBe(newTitleText);

    const newDescriptionText = "Other description";
    expect(newDescriptionText).not.toBe(dataset.description);
    await description.fill(newDescriptionText);
    expect(await description.inputValue()).toBe(newDescriptionText);

    const selectedTag = page.locator(
      'button[role="listitem"]:has-text("services")'
    );
    await selectedTag.waitFor();

    const tags = page.locator("form [name=tags]");

    await tags.selectOption({
      label: "environnement",
    });

    const newExtraFeferentiel = "Standard MC2019";
    expect(newExtraFeferentiel).not.toBe(dataset.extraFieldValues[0].value);
    await extraReferentiel.fill(newExtraFeferentiel);
    expect(await extraReferentiel.inputValue()).toBe(newExtraFeferentiel);

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest(`**/datasets/${dataset.id}/`),
      page.waitForResponse(`**/datasets/${dataset.id}/`),
      button.click(),
    ]);
    expect(request.method()).toBe("PUT");
    expect(response.status()).toBe(200);
    const json = await response.json();
    expect(json).toHaveProperty("id");
    expect(json.title).toBe(newTitleText);
    expect(json.description).toBe(newDescriptionText);
    expect(json.formats).toStrictEqual([
      {
        id: 1,
        name: "Fichier tabulaire (XLS, XLSX, CSV, ...)",
      },
      {
        id: 2,
        name: "Fichier SIG (Shapefile, ...)",
      },
    ]);
    expect(
      json.tags.findIndex((item) => item.name === "environnement") !== -1
    ).toBeTruthy();
    expect(json.extra_field_values[0].value).toBe(newExtraFeferentiel);
  });

  test("Does not see delete button", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);
    const deleteButton = page.locator(DELETE_DATASET_BUTTON_LOCATOR);
    await expect(deleteButton).not.toBeVisible();
  });

  test("Clears the url", async ({ page, dataset }) => {
    // Regression test: used to fail due to sending "" when server requires
    // null to indicate "no published URL".
    await page.goto(`/fiches/${dataset.id}/edit`);

    const url = page.locator("form [name=url]");
    // Simulate touching the field or unsetting a previous value.
    await url.fill("");
    expect(await url.inputValue()).toBe("");

    const button = page.locator("button[type='submit']");
    const [response] = await Promise.all([
      page.waitForResponse(`**/datasets/${dataset.id}/`),
      button.click(),
    ]);
    expect(response.status()).toBe(200);
    const json = await response.json();
    expect(json.url).toBe(null);
  });
});

test.describe("confirm before exit", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Should display a modal after clicking the exit button if changes has been made", async ({
    page,
    dataset,
  }) => {
    await page.goto(`/`);
    await page.goto(`/fiches/${dataset.id}/edit`);
    const title = page.locator("form [name=title]");

    // make change

    const newTitleText = "Other title";
    expect(newTitleText).not.toBe(dataset.title);
    await title.fill(newTitleText);

    // check if the modal is open

    await page.locator("[data-testid=exit-edit-form]").click();
    await page.locator("[id=stop-editing-form-modal]");

    // send changes to the api

    const button = await page.locator("text=Quitter sans sauvegarder");

    button.click();

    // check if the user has been redirected to the dataset detail page
    await page.waitForURL(`/fiches/${dataset.id}`);
  });

  test("Should NOT display a modal after clicking the exit button if NO changes has been made and should go to previous page ", async ({
    page,
    dataset,
  }) => {
    // Build user navigation history
    await page.goto(`/`);
    await page.goto(`/fiches/${dataset.id}/edit`);

    // Try to quit the form
    await page.locator("[data-testid=exit-edit-form]").click();

    // check if the user has been redirected to the dataset detail page
    await page.waitForURL(`/fiches/${dataset.id}`);
  });
});

test.describe("Edit as outside contributor", () => {
  test.describe("As a user", () => {
    test.use({ storageState: STATE_AUTHENTICATED_SANTE });

    test("Visits edit page as user from other org and gets permission denied", async ({
      page,
      dataset,
    }) => {
      await page.goto(`/fiches/${dataset.id}/edit`);
      await page.locator("form [name=title]").waitFor();
    });
  });

  test.describe("As an admin", () => {
    test.use({ storageState: STATE_AUTHENTICATED_ADMIN_SANTE });

    test("Visits edit page as admin from other org", async ({
      page,
      dataset,
    }) => {
      /**
       * [Regression test] Legitimate users outside the dataset's organization used
       * to not be able to access the page because we fetched their organization's
       * catalog, instead of the catalog of the dataset.
       */
      await page.goto(`/fiches/${dataset.id}/edit`);
      await page.locator("form [name=title]").waitFor();
    });
  });
});

test.describe("Edit dataset as admin", () => {
  test.use({ storageState: STATE_AUTHENTICATED_ADMIN });

  test("Deletes dataset via edit page", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);

    let confirmShown = false;
    page.on("dialog", async (dialog) => {
      expect(dialog.type()).toBe("confirm");
      confirmShown = true;
      await dialog.accept();
    });

    const deleteButton = page.locator(DELETE_DATASET_BUTTON_LOCATOR);

    await Promise.all([
      page.waitForRequest((request) => request.method() === "DELETE"),
      page.waitForResponse((response) => response.status() === 204),
      deleteButton.click(),
    ]);
    await page.waitForURL("/");
    expect(confirmShown).toBe(true);

    await page.goto(`/fiches/${dataset.id}`);
    const response = await page.waitForResponse(`**/datasets/${dataset.id}/`);
    expect(response.status()).toBe(404);
  });
});
