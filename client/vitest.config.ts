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
      $lib: path.resolve("./src/lib"),
      // Add any alias resolutions that should be mocked, because
      // they are not available unless SvelteKit runs.
      "$app/environment": path.resolve("./src/tests/app.environment.mock.ts"),
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
    deps: {
      inline: [
        // Address an issue raised by Vitest: "seems to be an ES Module but
        // shipped in a CommonJS package". No issue in the date-fns repository
        // about this to date.
        "date-fns",
      ],
    },
  },
});
