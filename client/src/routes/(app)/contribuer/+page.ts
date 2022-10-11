import type { PageLoad } from "./$types";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { get } from "svelte/store";
import { account } from "src/lib/stores/auth";
import { apiToken as apiTokenStore } from "$lib/stores/auth";
import { Maybe } from "$lib/util/maybe";
import { siteSection } from "src/lib/stores/layout/title";

export const load: PageLoad = async ({ fetch }) => {
  const title = "Contribuer une fiche de jeu de données";

  siteSection.set(title);

  const apiToken = get(apiTokenStore);
  const siret = Maybe.expect(get(account), "$account").organizationSiret;

  const [catalog, tags, licenses, filtersInfo] = await Promise.all([
    getCatalogBySiret({ fetch, apiToken, siret }),
    getTags({ fetch, apiToken }),
    getLicenses({ fetch, apiToken }),
    getDatasetFiltersInfo({ fetch, apiToken }),
  ]);

  return {
    title,
    catalog,
    tags,
    licenses,
    filtersInfo,
  };
};
