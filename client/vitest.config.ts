/// <reference types="vitest" />
import path from "path";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { config as baseConfig } from "./vite.config";

export default defineConfig({
  ...baseConfig,
  resolve: {
    alias: {
      ...baseConfig?.resolve?.alias,
      // Add any alias resolutions that should be mocked, because
      // they are not available unless SvelteKit runs.
      "$app/environment": path.resolve("./src/tests/app.env.mock.ts"),
      "$app/navigation": path.resolve("./src/tests/app.navigation.mock.ts"),
    },
  },
  plugins: [
    svelte({
      hot: !process.env.VITEST,
    }),
  ],
  test: {
    globals: true,
    environment: "node",
    exclude: [
      "**/e2e/**",
      "**/node_modules/**",
      "**/dist/**",
      "**/.{idea,git,cache,output,temp}/**",
    ],
    setupFiles: [path.resolve("./src/tests/setup.ts")],
  },
});
