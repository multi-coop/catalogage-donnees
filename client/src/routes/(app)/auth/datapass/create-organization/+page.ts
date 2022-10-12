import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";

export const ssr = true;

export const load: PageLoad = () => {
  return {
    title: `Connexion avec MonComptePro : aucune organisation enregistrée - ${SITE_TITLE}`,
  };
};
