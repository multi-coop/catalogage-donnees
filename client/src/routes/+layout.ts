import type { LayoutLoad } from "./$types";
import { get } from "svelte/store";
import { redirect } from "@sveltejs/kit";
import { account } from "$lib/stores/auth";
import { NON_AUTH_GUARDED_PAGES } from "src/constants";
import { Maybe } from "$lib/util/maybe";

// NOTE: SSR usage is aimed at improving SEO, but most of our pages are
// hidden behind authentication.
// SSR will be enabled selectively on appropriate pages.
// This also happens to simplify the e2e test setup, as auth state
// for private pages can then be exclusively managed in the browser.
// See: https://github.com/etalab/catalogage-donnees/pull/143
export const ssr = false;

export const load: LayoutLoad = async ({ url }) => {
  // Force-redirect to the login page if an unauthenticated user
  // is attempting to access a protected page.
  if (NON_AUTH_GUARDED_PAGES.includes(url.pathname)) {
    return {};
  }

  if (Maybe.Some(get(account))) {
    return {};
  }

  throw redirect(302, "/");
};
