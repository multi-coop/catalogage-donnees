import type { DataFormat } from "src/definitions/dataformat";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequestOrFail } from "../fetch";

type Options = {
  fetch: Fetch;
  apiToken: string;
};

type GetDataFormats = (opts: Options) => Promise<DataFormat[]>;

export const getDataFormats: GetDataFormats = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/dataformats/`;
  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await makeApiRequestOrFail(fetch, request);
  return response.json();
};

export const postDataFormat = async ({
  fetch,
  apiToken,
  value,
}: Options & { value: string }): Promise<DataFormat> => {
  const body = JSON.stringify({ value });
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url, {
    method: "POST",
    headers: new Headers([
      ["Content-Type", "application/json"],
      ...getHeaders(apiToken),
    ]),
    body,
  });

  const response = await makeApiRequestOrFail(fetch, request);

  return (await response.json()) as DataFormat;
};
