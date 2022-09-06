import { test, expect } from "@playwright/test";
import { UPDATE_FREQUENCY_LABELS } from "../../constants.js";
import { STATE_AUTHENTICATED } from "./constants.js";

test.describe("Basic form submission", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the contribution page", async ({ page }) => {
    const titleText = "Un nom de jeu de données";
    const descriptionText = "Une longue\ndescription de jeu\nde données";
    const geographicalCoverageText = "Europe continentale";
    const producerEmailText = "un.service@exemple.gouv.fr";
    const contactEmail1Text = "contact1@mydomain.org";
    const contactEmail2Text = "contact2@mydomain.org";
    const lastUpdatedAtDate = "2000-05-05";
    const serviceText = "Ministère de l'écologie";
    const technicalSourceText = "foo/bar";
    const urlText = "https://data.gouv.fr/datasets/example";
    const tagName = "services des eaux";
    const licenseText = "Licence Ouverte";

    await page.goto("/contribuer");

    // "Information Générales" section

    expect(
      page
        .locator("a.fr-sidemenu__link", { hasText: "Informations générales" })
        .first()
    ).toHaveAttribute("aria-current", "page");
    const title = page.locator("form [name=title]");
    await title.fill(titleText);
    expect(await title.inputValue()).toBe(titleText);

    const description = page.locator("form [name=description]");
    await description.fill(descriptionText);
    expect(await description.inputValue()).toBe(descriptionText);

    const geographicalCoverage = page.locator(
      "form [name=geographicalCoverage]"
    );
    await geographicalCoverage.fill(geographicalCoverageText);
    expect(await geographicalCoverage.inputValue()).toBe(
      geographicalCoverageText
    );

    // "Sources et formats" section

    const apiFormat = page.locator("label[for=dataformats-api]");
    await apiFormat.check();
    expect(await page.isChecked("input[value=api]")).toBeTruthy();

    const technicalSource = page.locator("form [name=technicalSource]");
    await technicalSource.fill(technicalSourceText);
    expect(await technicalSource.inputValue()).toBe(technicalSourceText);

    // "Contacts" section

    const service = page.locator("form [name=service]");
    await service.fill(serviceText);
    expect(await service.inputValue()).toBe(serviceText);

    const producerEmail = page.locator("label[for=producerEmail]");
    await producerEmail.fill(producerEmailText);
    expect(await producerEmail.inputValue()).toBe(producerEmailText);

    const contactEmail1 = page.locator("[id='contactEmails-0']");
    await contactEmail1.fill(contactEmail1Text);
    expect(await contactEmail1.inputValue()).toBe(contactEmail1Text);

    await page.locator("text='Ajouter un contact'").click();
    const contactEmail2 = page.locator("[id='contactEmails-1']");
    await contactEmail2.fill(contactEmail2Text);
    expect(await contactEmail2.inputValue()).toBe(contactEmail2Text);

    // "Mise à jour" section

    const lastUpdatedAt = page.locator("form [name=lastUpdatedAt]");
    await lastUpdatedAt.fill("2000-05-05");
    expect(await lastUpdatedAt.inputValue()).toBe(lastUpdatedAtDate);

    const updateFrequency = page.locator("form [name=updateFrequency]");
    await updateFrequency.selectOption({
      label: UPDATE_FREQUENCY_LABELS.daily,
    });

    // "Accès aux données" section

    const url = page.locator("form [name=url]");
    await url.fill(urlText);
    expect(await url.inputValue()).toBe(urlText);

    const license = page.locator("form [name=license]");
    await license.fill(licenseText);
    expect(await license.inputValue()).toBe(licenseText);

    // "Mots clés" section

    const tags = page.locator("form [name=tags]");

    await tags.selectOption({
      label: tagName,
    });

    const selectedTag = page.locator(
      'button[role="listitem"]:has-text("services des eaux")'
    );
    await selectedTag.waitFor();

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/"),
      page.waitForResponse("**/datasets/"),
      button.click(),
    ]);
    expect(
      page
        .locator("a.fr-sidemenu__link", { hasText: "Accès aux données" })
        .first()
    ).toHaveAttribute("aria-current", "page");
    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(201);
    const json = await response.json();
    expect(json.title).toBe(titleText);
    expect(json.description).toBe(descriptionText);
    expect(json.geographical_coverage).toBe("Europe continentale");
    expect(json.formats).toStrictEqual(["api"]);
    expect(json.producer_email).toBe(producerEmailText);
    expect(json.contact_emails).toEqual([contactEmail1Text, contactEmail2Text]);
    expect(json).toHaveProperty("id");
    expect(json.technical_source).toBe(technicalSourceText);
    expect(json.update_frequency).toBe("daily");
    expect(json.last_updated_at).toEqual("2000-05-05T00:00:00+00:00");
    expect(json.service).toBe(serviceText);
    expect(json.url).toBe(urlText);
    expect(json.license).toBe(licenseText);

    const hasTag = json.tags.findIndex((item) => item.name === tagName) !== -1;
    expect(hasTag).toBeTruthy();

    await page.locator("text='Modifier'").waitFor();
  });

  test("Navigates on page and sees active sidebar item change", async ({
    page,
  }) => {
    await page.goto("/contribuer");

    const activeSidebarItem = page.locator(
      "[aria-label='Menu latéral'] [aria-current=page]"
    );

    // Initial state.
    await expect(activeSidebarItem).toHaveText("Informations générales");

    // Scroll to bottom.
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await expect(activeSidebarItem).toHaveText("Accès aux données");

    // Move to a particular section using click.
    // Purposefully test a small-size section: it should become active
    // even if the next section is fairly high on the page.
    await page.click(
      "[aria-label='Menu latéral'] >> text='Mot-clés thématiques'"
    );
    await expect(activeSidebarItem).toHaveText("Mot-clés thématiques");

    // Move up 1/4th of the window, should make previous section active.
    await page.evaluate(() => window.scrollBy(0, -window.innerHeight / 4));
    await expect(activeSidebarItem).toHaveText("Sources et formats");
  });

  test.describe("confirm before exit", () => {
    test.use({ storageState: STATE_AUTHENTICATED });

    test("Should display a modal after clicking the exit button if changes has been made", async ({
      page,
    }) => {
      await page.goto(`/`);
      await page.goto("/contribuer");
      const title = page.locator("form [name=title]");

      // make change

      const newTitleText = "Other title";
      await title.fill(newTitleText);

      // check if the modal is open

      await page.locator("[data-testid=exit-contribution-form]").click();
      await page.locator("[id=confirm-stop-contributing-modal]");

      // send changes to the api

      const button = await page.locator("text=Quitter sans sauvegarder");

      button.click();

      // check if the user has been redirected to the home page
      await page.waitForURL("/");
    });

    test("Should NOT display a modal after clicking the exit button if NO changes has been made and should go to previous page ", async ({
      page,
    }) => {
      // Build user navigation history
      await page.goto(`/`);
      await page.goto(`/contribuer`);

      // Try to quit the form
      await page.locator("[data-testid=exit-contribution-form]").click();

      // check if the user has been redirected to the home page
      await page.waitForURL("/");
    });
  });
});
