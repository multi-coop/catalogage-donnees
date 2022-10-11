import type { PageLoad } from "./$types";
import { get } from "svelte/store";
import { getDatasetByID } from "$lib/repositories/datasets";
import { getCatalogBySiret } from "$lib/repositories/catalogs";
import { Maybe } from "$lib/util/maybe";
import { apiToken as apiTokenStore } from "$lib/stores/auth";
import { siteSection } from "$lib/stores/layout/title";

export const load: PageLoad = async ({ fetch, params }) => {
  const apiToken = get(apiTokenStore);

  const dataset = await getDatasetByID({
    fetch,
    apiToken,
    id: params.id,
  });

  siteSection.set(
    Maybe.Some(dataset) ? dataset.title : "Fiche de jeu de données"
  );

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
