import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { get } from "svelte/store";
import { account } from "src/lib/stores/auth";
import { apiToken as apiTokenStore } from "$lib/stores/auth";
import { Maybe } from "$lib/util/maybe";
import { getDataFormats } from "src/lib/repositories/dataformat";

export const load: PageLoad = async ({ fetch }) => {
  const apiToken = get(apiTokenStore);
  const siret = Maybe.expect(get(account), "$account").organizationSiret;

  const [catalog, tags, licenses, filtersInfo, formats] = await Promise.all([
    getCatalogBySiret({ fetch, apiToken, siret }),
    getTags({ fetch, apiToken }),
    getLicenses({ fetch, apiToken }),
    getDatasetFiltersInfo({ fetch, apiToken }),
    getDataFormats({ fetch, apiToken }),
  ]);

  return {
    title: `${SITE_TITLE} - Contribuer une fiche de jeu de données`,
    catalog,
    tags,
    licenses,
    filtersInfo,
    formats,
  };
};
