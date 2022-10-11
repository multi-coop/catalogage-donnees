import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { getDatasets } from "$lib/repositories/datasets";
import { apiToken } from "$lib/stores/auth";
import { siteSection } from "$lib/stores/layout/title";
import { getPageFromParams } from "$lib/util/pagination";
import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
import { toFiltersValue } from "src/lib/transformers/datasetFilters";

export const load: PageLoad = async ({ fetch, url }) => {
  siteSection.set("Rechercher un jeu de données");

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
    paginatedDatasets,
    filtersInfo,
    filtersValue,
    currentPage: page,
    q,
  };
};
