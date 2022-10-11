import type { PageLoad } from "./$types";
import { sections } from "$lib/stores/layout/title";

export const ssr = true;

export const load: PageLoad = () => {
  sections.set(["Connexion"]);
};
