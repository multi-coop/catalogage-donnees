import type { PageLoad } from "./$types";
import { siteSection } from "$lib/stores/layout/title";
import { HOME_SECTION_NAME } from "src/constants";

export const load: PageLoad = () => {
  siteSection.set(HOME_SECTION_NAME);
};
