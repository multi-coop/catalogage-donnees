import path from "path";
import dotenv from "dotenv";
import type { PlaywrightTestConfig } from "@playwright/test";
import type { AppTestArgs } from "src/tests/e2e/fixtures";

dotenv.config({
  path: path.resolve("..", ".env"),
});

const config: PlaywrightTestConfig<AppTestArgs> = {
  testDir: "./tests/e2e/",
  globalSetup: "./tests/e2e/global-setup.ts",
  retries: 3,
  use: {
    baseURL: "http://localhost:3000",
    browserName: "firefox",
    headless: true,
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },
};

export default config;
