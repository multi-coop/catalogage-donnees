import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";

export const load: PageLoad = () => {
  return {
    title: `Connexion - ${SITE_TITLE}`,
  };
};
