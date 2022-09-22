import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED, STATE_AUTHENTICATED_SANTE } from "./constants.js";
import { test } from "./fixtures.js";

test.describe("Dataset details", () => {
  test.describe("As a user in same organization than dataset", () => {
    test.use({ storageState: STATE_AUTHENTICATED });

    test("Displays dataset details", async ({ page, dataset }) => {
      await page.goto(`/fiches/${dataset.id}`);

      const title = page.locator("h1");
      await expect(title).toHaveText(dataset.title);

      const description = page.locator("[data-testid=dataset-description]");
      await expect(description).toHaveText(dataset.description);
    });

    test("The edit button is shown", async ({ page, dataset }) => {
      await page.goto(`/fiches/${dataset.id}`);
      const editUrl = page.locator("text='Modifier'");
      await expect(editUrl).toBeVisible();
      expect(await editUrl.getAttribute("href")).toBe(
        `/fiches/${dataset.id}/edit`
      );
    });
  });

  test.describe("As a user in different organization", () => {
    test.use({ storageState: STATE_AUTHENTICATED_SANTE });
    test("The edit button is not shown", async ({ page, dataset }) => {
      await page.goto(`/fiches/${dataset.id}`);
      await expect(page.locator("text='Modifier'")).toBeHidden();
    });
  });
});
