import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { SITE_TITLE } from "src/constants";
import { getDatasets } from "$lib/repositories/datasets";
import { apiToken } from "$lib/stores/auth";
import { getPageFromParams } from "$lib/util/pagination";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { toFiltersValue } from "src/lib/transformers/datasetFilters";

export const load: PageLoad = async ({ fetch, url }) => {
  const page = getPageFromParams(url.searchParams);
  const q = url.searchParams.get("q") || "";
  const filtersValue = toFiltersValue(url.searchParams);

  const token = get(apiToken);

  const [paginatedDatasets, filtersInfo] = await Promise.all([
    getDatasets({
      fetch,
      apiToken: token,
      page,
      q,
      filters: filtersValue,
    }),
    getDatasetFiltersInfo({ fetch, apiToken: token }),
  ]);

  return {
    title: `Rechercher un jeu de données - ${SITE_TITLE}`,
    paginatedDatasets,
    filtersInfo,
    filtersValue,
    currentPage: page,
    q,
  };
};
