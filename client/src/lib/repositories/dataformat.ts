import type { DataFormat } from "src/definitions/dataformat";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequestOrFail } from "../fetch";

type GetDataFormats = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<DataFormat[]>;

export const getDataFormats: GetDataFormats = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/dataformats/`;
  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await makeApiRequestOrFail(fetch, request);
  return response.json();
};
