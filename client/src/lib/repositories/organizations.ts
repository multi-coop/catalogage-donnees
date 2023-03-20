import type { Fetch } from "src/definitions/fetch";
import type { Organization } from "src/definitions/organization";
import { getApiUrl, getHeaders, makeApiRequest } from "../fetch";
import { Maybe } from "../util/maybe";

type GetOrganizations = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Maybe<Organization[]>>;

export const getOrganizations: GetOrganizations = async ({
  fetch,
  apiToken,
}) => {
  const url = `${getApiUrl()}/organizations/`;

  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) => {
    const data = await response.json();
    console.log(data);

    return data;
  });
};
