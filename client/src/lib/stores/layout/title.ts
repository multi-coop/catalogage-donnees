import { writable, derived } from "svelte/store";
import { Maybe } from "$lib/util/maybe";
import { SITE_TITLE } from "src/constants";

export const siteSection = writable<Maybe<string>>(null);

export const pageTitle = derived(siteSection, (siteSectionValue): string => {
  if (Maybe.Some(siteSectionValue)) {
    return `${siteSectionValue} - ${SITE_TITLE}`;
  } else {
    return SITE_TITLE;
  }
});
