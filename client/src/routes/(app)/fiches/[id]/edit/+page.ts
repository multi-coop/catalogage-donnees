import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getDatasetByID } from "$lib/repositories/datasets";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { apiToken as apiTokenStore } from "$lib/stores/auth";
import { Maybe } from "$lib/util/maybe";

export const load: PageLoad = async ({ fetch, params }) => {
  const apiToken = get(apiTokenStore);

  const dataset = await getDatasetByID({ fetch, apiToken, id: params.id });

  const [catalog, tags, licenses, filtersInfo] = await Promise.all([
    Maybe.map(dataset, (dataset) =>
      getCatalogBySiret({
        fetch,
        apiToken,
        siret: dataset.catalogRecord.organization.siret,
      })
    ),
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
