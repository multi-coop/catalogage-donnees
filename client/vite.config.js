import { defineConfig } from "vite";
import path from "path";
import dotenv from "dotenv";
import purgecss from "@fullhuman/postcss-purgecss";
import cssnano from "cssnano";

// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env"),
});

const postcssPlugins = [];

if (process.env.NODE_ENV === "production") {
  postcssPlugins.push(
    purgecss({
      content: ["./src/**/*.html", "./src/**/*.svelte"],
      safelist: [
        /svelte-/, // Don't purge custom CSS defined in Svelte component <style> sections
      ],
    })
  );
  postcssPlugins.push(cssnano());
}

/**
 * @type {import('vite').UserConfig}
 */
export const config = {
  envDir: path.resolve(".."),
  resolve: {
    alias: {
      src: path.resolve("./src"),
      $lib: path.resolve("./src/lib"),
      "@js": path.resolve("./src/lib/js"),
    },
  },
  css: {
    postcss: {
      plugins: postcssPlugins,
    },
  },
};

export default defineConfig(config);
