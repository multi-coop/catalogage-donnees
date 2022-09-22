import {
  expect,
  firefox,
  type FullConfig,
  type Browser,
} from "@playwright/test";

import {
  ADMIN_EMAIL,
  ADMIN_PASSWORD,
  STATE_AUTHENTICATED,
  STATE_AUTHENTICATED_ADMIN,
  STATE_AUTHENTICATED_SANTE,
  TEST_EMAIL,
  TEST_EMAIL_SANTE,
  TEST_PASSWORD,
  TEST_PASSWORD_SANTE,
} from "./constants.js";
import type { AppTestArgs } from "./fixtures.js";

export default async function globalSetup(
  config: FullConfig<AppTestArgs>
): Promise<void> {
  const browser = await firefox.launch({
    headless: true,
  });

  await saveAuthenticatedState(browser, config, {
    email: TEST_EMAIL,
    password: TEST_PASSWORD,
    path: STATE_AUTHENTICATED,
  });

  await saveAuthenticatedState(browser, config, {
    email: TEST_EMAIL_SANTE,
    password: TEST_PASSWORD_SANTE,
    path: STATE_AUTHENTICATED_SANTE,
  });

  await saveAuthenticatedState(browser, config, {
    email: ADMIN_EMAIL,
    password: ADMIN_PASSWORD,
    path: STATE_AUTHENTICATED_ADMIN,
  });

  await browser.close();
}

type SaveOptions = {
  email: string;
  password: string;
  path: string;
};

async function saveAuthenticatedState(
  browser: Browser,
  config: FullConfig,
  { email, password, path }: SaveOptions
) {
  const page = await browser.newPage({
    baseURL: config.projects[0].use.baseURL,
  });
  await page.goto("/login");
  await page.fill("input[name='email']", email);
  await page.fill("input[name='password']", password);
  await page.locator("button[type='submit']").click();
  const response = await page.waitForResponse("**/auth/login/");
  expect(response.status()).toBe(200); // If this fails, ensure you ran `make initdata`.
  await page.waitForURL("/");
  await page.context().storageState({ path });
  await page.close();
}
