import { writable, derived } from "svelte/store";
import { Maybe } from "$lib/util/maybe";
import { siteTitle } from "$lib/site";

export const siteSection = writable<Maybe<string>>(null);

export const pageTitle = derived(siteSection, (siteSectionValue): string => {
  if (Maybe.Some(siteSectionValue)) {
    return `${siteSectionValue} - ${siteTitle}`;
  } else {
    return siteTitle;
  }
});
