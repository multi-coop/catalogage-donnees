import type { PageLoad } from "./$types";
import { sections } from "$lib/stores/layout/title";
import { homeSectionName } from "$lib/site";

export const load: PageLoad = () => {
  sections.set([homeSectionName]);
};
