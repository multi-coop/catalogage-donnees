import type { PageLoad } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getDatasetByID, updateDataset } from "$lib/repositories/datasets";
import type { Tag } from "src/definitions/tag";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";

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
