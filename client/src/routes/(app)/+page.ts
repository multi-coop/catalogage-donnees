import type { PageLoad } from "./$types";
import { siteSection } from "$lib/stores/layout/title";
import { homeSectionName } from "$lib/site";

export const load: PageLoad = () => {
  siteSection.set(homeSectionName);
};
