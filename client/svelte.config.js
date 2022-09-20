import adapter from "@sveltejs/adapter-node";
import preprocess from "svelte-preprocess";

const VITE_SERVER_MODE = process.env.VITE_SERVER_MODE;

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: preprocess(),

  kit: {
    adapter: adapter({ precompress: true }),

    csp: {
      directives: {
        "default-src": ["self"],
        "manifest-src": ["self", "data:"],
        "connect-src":
          // Allow XHR requests to API during local development
          VITE_SERVER_MODE === "live" ? undefined : ["self", "localhost:3579"],
        "font-src": [
          "self",
          "data:", // E.g. inline icon fonts (us or DSFR)
        ],
        "img-src": [
          "self",
          "data:", // E.g. DSFR inline images
        ],
      },
    },
  },
};

export default config;
