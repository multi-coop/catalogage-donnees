import type { PageLoad } from "./$types";
import { get } from "svelte/store";
import { getDatasetByID } from "$lib/repositories/datasets";
import { getCatalogBySiret } from "$lib/repositories/catalogs";
import { Maybe } from "$lib/util/maybe";
import { apiToken as apiTokenStore } from "$lib/stores/auth";

export const load: PageLoad = async ({ fetch, params }) => {
  const apiToken = get(apiTokenStore);

  const dataset = await getDatasetByID({
    fetch,
    apiToken,
    id: params.id,
  });

  const catalog = await Maybe.map(dataset, (dataset) =>
    getCatalogBySiret({
      fetch,
      apiToken,
      siret: dataset.catalogRecord.organization.siret,
    })
  );

  return {
    catalog,
    dataset,
  };
};
