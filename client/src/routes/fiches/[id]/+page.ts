import type { PageLoad } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getDatasetByID } from "$lib/repositories/datasets";
import { apiToken } from "$lib/stores/auth";

export const load: PageLoad = async ({ fetch, params }) => {
  const dataset = await getDatasetByID({
    fetch,
    apiToken: get(apiToken),
    id: params.id,
  });

  return {
  dataset,
};
};
