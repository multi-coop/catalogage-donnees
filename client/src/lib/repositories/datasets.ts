import type {
  Dataset,
  DatasetCreateData,
  DatasetUpdateData,
} from "src/definitions/datasets";
import type { DatasetFiltersValue } from "src/definitions/datasetFilters";
import type { Fetch } from "src/definitions/fetch";
import type { Paginated } from "src/definitions/pagination";
import { DATASETS_PER_PAGE } from "src/constants";
import {
  getHeaders,
  getApiUrl,
  makeApiRequest,
  makeApiRequestOrFail,
} from "$lib/fetch";
import { toQueryString } from "$lib/util/urls";
import { toDataset, toPayload } from "$lib/transformers/dataset";
import { toPaginated } from "$lib/transformers/pagination";
import { toFiltersParams } from "$lib/transformers/datasetFilters";
import { Maybe } from "$lib/util/maybe";
import type { QueryParamRecord } from "src/definitions/url";
import { getFakeDataset } from "src/tests/factories/dataset";

type GetDatasetByID = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
}) => Promise<Dataset>;

export const getDatasetByID: GetDatasetByID = async ({
  fetch,
  apiToken,
  id,
}) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  try {
    const response = await makeApiRequestOrFail(fetch, request);
    return toDataset(await response.json());
  } catch (error) {
    return Promise.reject(error);
  }
};

type GetDatasets = (opts: {
  fetch: Fetch;
  apiToken: string;
  page: number;
  q?: string;
  filters?: Maybe<DatasetFiltersValue>;
}) => Promise<Maybe<Paginated<Dataset>>>;

export const getDatasets: GetDatasets = async ({
  fetch,
  apiToken,
  page,
  q,
  filters,
}) => {
  const queryItems: QueryParamRecord = [
    ["page_number", page.toString()],
    ["page_size", DATASETS_PER_PAGE.toString()],
  ];

  if (Maybe.Some(q) && q) {
    queryItems.push(["q", q]);
  }

  if (Maybe.Some(filters)) {
    queryItems.push(...toFiltersParams(filters));
  }

  const queryString = toQueryString(queryItems);
  const url = `${getApiUrl()}/datasets/${queryString}`;

  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) => {
    const data = await response.json();
    return toPaginated(data, (item) => toDataset(item));
  });
};

type CreateDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  data: DatasetCreateData;
}) => Promise<Maybe<Dataset>>;

export const createDataset: CreateDataset = async ({
  fetch,
  apiToken,
  data,
}) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url, {
    method: "POST",
    headers: new Headers([
      ["Content-Type", "application/json"],
      ...getHeaders(apiToken),
    ]),
    body,
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) =>
    toDataset(await response.json())
  );
};

type UpdateDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
  data: DatasetUpdateData;
}) => Promise<Maybe<Dataset>>;

export const updateDataset: UpdateDataset = async ({
  fetch,
  apiToken,
  id,
  data,
}) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    method: "PUT",
    headers: new Headers([
      ["Content-Type", "application/json"],
      ...getHeaders(apiToken),
    ]),
    body,
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) =>
    toDataset(await response.json())
  );
};

type DeleteDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
}) => Promise<void>;

export const deleteDataset: DeleteDataset = async ({ fetch, apiToken, id }) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    method: "DELETE",
    headers: new Headers(getHeaders(apiToken)),
  });
  await makeApiRequest(fetch, request);
};
