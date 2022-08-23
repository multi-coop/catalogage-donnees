import { get } from "svelte/store";
import type { LoadOutput } from "@sveltejs/kit";
import { user } from "../stores/auth";
import { PUBLIC_PAGES } from "src/constants";
import { Maybe } from "$lib/util/maybe";

/**
 * Force-redirect to the login page if an unauthenticated user
 * is attempting to access a protected page.
 */
export const authGuard = (url: URL): LoadOutput => {
  if (PUBLIC_PAGES.includes(url.pathname)) {
    return {};
  }

  if (Maybe.Some(get(user))) {
    return {};
  }

  return {
    status: 302,
    redirect: "/",
  };
};
