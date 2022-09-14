import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getDatasetByID } from "$lib/repositories/datasets";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { apiToken as apiTokenStore, account } from "$lib/stores/auth";
import { Maybe } from "$lib/util/maybe";

export const load: PageLoad = async ({ fetch, params }) => {
  const apiToken = get(apiTokenStore);
  const siret = Maybe.expect(get(account), "$account").organizationSiret;

  const [catalog, dataset, tags, licenses, filtersInfo] = await Promise.all([
    getCatalogBySiret({ fetch, apiToken, siret }),
    getDatasetByID({ fetch, apiToken, id: params.id }),
    getTags({ fetch, apiToken }),
    getLicenses({ fetch, apiToken }),
    getDatasetFiltersInfo({ fetch, apiToken }),
  ]);

  return {
    catalog,
    dataset,
    tags,
    licenses,
    filtersInfo,
  };
};
