import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";

export const prerender = true;
export const ssr = true;

export const load: PageLoad = () => {
  return {
    title: `Vie privée - ${SITE_TITLE}`,
  };
};
