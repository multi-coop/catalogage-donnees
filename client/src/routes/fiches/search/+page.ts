import type { PageLoad } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getDatasets } from "$lib/repositories/datasets";
import { apiToken } from "$lib/stores/auth";
import { getPageFromParams } from "$lib/util/pagination";
import { page as pageStore } from "$app/stores";
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
  paginatedDatasets,
  filtersInfo,
  filtersValue,
  currentPage: page,
  q,
};
};
