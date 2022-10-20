import { get } from "svelte/store";
import { redirect } from "@sveltejs/kit";
import { account } from "$lib/stores/auth";
import { NON_AUTH_GUARDED_PAGES } from "src/constants";
import { Maybe } from "$lib/util/maybe";
import type { LayoutLoad } from ".svelte-kit/types/src/routes/$types";

export const authGuard: LayoutLoad = async ({ url }) => {
  // Force-redirect to the home page if an unauthenticated user
  // is attempting to access a protected page.
  if (NON_AUTH_GUARDED_PAGES.includes(url.pathname)) {
    return {};
  }

  if (Maybe.Some(get(account))) {
    return {};
  }

  throw redirect(302, "/");
};
