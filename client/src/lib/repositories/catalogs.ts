import type { Catalog } from "src/definitions/catalogs";
import type { Fetch } from "src/definitions/fetch";
import {
  getApiUrl,
  getHeaders,
  makeApiRequest,
  makeApiRequestOrFail,
} from "../fetch";
import { toCatalog } from "../transformers/catalogs";
import { Maybe } from "../util/maybe";

type GetCatalogBySiret = (opts: {
  fetch: Fetch;
  apiToken: string;
  siret: string;
}) => Promise<Maybe<Catalog>>;

export const getCatalogBySiret: GetCatalogBySiret = async ({
  fetch,
  apiToken,
  siret,
}) => {
  const url = `${getApiUrl()}/catalogs/${siret}/`;

  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) => {
    const data = await response.json();
    return toCatalog(data);
  });
};

type GetCatalogs = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Catalog[]>;

export const getCatalogs: GetCatalogs = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/catalogs/`;

  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await makeApiRequestOrFail(fetch, request);
  const data = await response.json();
  return data
    .map(toCatalog)
    .sort((a: Catalog, b: Catalog) => {

      if (a.organization.name < b.organization.name) {
        return -1;
      }
      if (a.organization.name > b.organization.name) {
        return 1;
      }
      return 0;
    })
    .filter((item) => item.organization.siret !== "00000000000000");
};
