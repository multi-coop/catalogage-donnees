import type { Handle } from "@sveltejs/kit";
import { maybePatchDataUrl } from "$lib/fetch";
import { STATIC_PAGES } from "./constants";

// See: https://kit.svelte.dev/docs/hooks#handle
export const handle: Handle = async ({ event, resolve }) => {
  let response = await resolve(event, {
    // NOTE: SSR usage is aimed at improving SEO, so we focus on static pages
    // that do not depend on user authentication.
    // This also happens to simplify the e2e test setup, as auth state
    // for private pages can then be exclusively managed in the browser.
    // See: https://github.com/etalab/catalogage-donnees/pull/143
    ssr: STATIC_PAGES.includes(event.url.pathname),
  });

  response = await maybePatchDataUrl(response, event.url);

  return response;
};
