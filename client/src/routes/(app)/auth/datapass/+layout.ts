import type { LayoutLoad } from "./$types";
import { sections } from "$lib/stores/layout/title";

export const load: LayoutLoad = () => {
  sections.set(["Connexion avec MonComptePro"]);
};
