import type { LayoutLoad } from "./$types";
import { authGuard } from "src/lib/util/auth";

// NOTE: SSR usage is aimed at improving SEO, but most of our pages are
// hidden behind authentication.
// SSR will be enabled selectively on appropriate pages.
// This also happens to simplify the e2e test setup, as auth state
// for private pages can then be exclusively managed in the browser.
// See: https://github.com/etalab/catalogage-donnees/pull/143
export const ssr = false;
export const load: LayoutLoad = authGuard;
