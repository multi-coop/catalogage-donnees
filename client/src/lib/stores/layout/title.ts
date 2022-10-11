import { writable, derived } from "svelte/store";
import { siteTitle } from "$lib/site";

export const sections = writable<string[]>([]);

export const pageTitle = derived(sections, (sectionsValue) => {
  return [...sectionsValue, siteTitle].join(" - ");
});
