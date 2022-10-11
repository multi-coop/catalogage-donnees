import type { PageLoad } from "./$types";
import { siteSection } from "$lib/stores/layout/title";

export const ssr = true;

export const load: PageLoad = () => {
  siteSection.set("Connexion");
};
