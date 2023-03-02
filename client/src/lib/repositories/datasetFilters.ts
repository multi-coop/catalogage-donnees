import type { DatasetFiltersInfo } from "src/definitions/datasetFilters";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequestOrFail } from "../fetch";
import { toFiltersInfo } from "../transformers/datasetFilters";

type GetDatasetFiltersInfo = (opts: {
  fetch: Fetch;
  apiToken: string;
  organizationSiret?: string | null;
}) => Promise<DatasetFiltersInfo>;

export const getDatasetFiltersInfo: GetDatasetFiltersInfo = async ({
  fetch,
  apiToken,
  organizationSiret,
}) => {
  const urlBase = `${getApiUrl()}/datasets/filters`;

  const url = organizationSiret
    ? `${urlBase}?organization_siret=${organizationSiret}`
    : `${urlBase}/`;

  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = await (await makeApiRequestOrFail(fetch, request)).json();

  return toFiltersInfo(response);
};
