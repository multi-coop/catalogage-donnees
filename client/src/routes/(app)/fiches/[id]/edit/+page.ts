import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";
import { getCatalogBySiret } from "src/lib/repositories/catalogs";
import { getDatasetByID } from "$lib/repositories/datasets";
import { getTags } from "src/lib/repositories/tags";
import { getLicenses } from "src/lib/repositories/licenses";
import { getDataFormats } from "src/lib/repositories/dataformat";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { apiToken as apiTokenStore } from "$lib/stores/auth";
import { Maybe } from "$lib/util/maybe";
import { error } from "@sveltejs/kit";

export const load: PageLoad = async ({ fetch, params }) => {
  const apiToken = get(apiTokenStore);

  try {
    const dataset = await getDatasetByID({ fetch, apiToken, id: params.id });

    const [catalog, tags, licenses, filtersInfo, formats] = await Promise.all([
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
      getDataFormats({ fetch, apiToken }),
    ]);

    return {
      title: `Modifier la fiche de jeu de données - ${SITE_TITLE}`,
      catalog,
      dataset,
      tags,
      licenses,
      filtersInfo,
      formats,
    };
  } catch (response) {
    if (response.status === 403) {
      throw error(404);
    }
  }

  return {
    title: `Modifier la fiche de jeu de données - ${SITE_TITLE}`,
    catalog: undefined,
    dataset: undefined,
    tags: undefined,
    licenses: undefined,
    filtersInfo: undefined,
    dataformats: undefined,
  };
};
