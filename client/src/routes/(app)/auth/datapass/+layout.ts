import type { LayoutLoad } from "./$types";
import { siteSection } from "$lib/stores/layout/title";

export const load: LayoutLoad = () => {
  siteSection.set("Connexion avec MonComptePro");
};
