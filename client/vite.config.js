import { defineConfig } from "vite";
import { sveltekit } from "@sveltejs/kit/vite";
import path from "path";
import dotenv from "dotenv";
import gzip from "rollup-plugin-gzip";
import cssnano from "cssnano";
// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env"),
});

const postcssPlugins = [];

if (process.env.NODE_ENV === "production") {
  postcssPlugins.push(cssnano());
}

/**
 * @type {import('vite').UserConfig}
 */
export const config = {
  plugins: [sveltekit(), gzip()],
  envDir: path.resolve(".."),
  server: {
    port: 3000,
  },
  preview: {
    port: 3000,
  },
  resolve: {
    alias: {
      src: path.resolve("./src"),
    },
  },
  css: {
    postcss: {
      plugins: postcssPlugins,
    },
  },
};

export default defineConfig(config);
