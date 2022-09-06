import type { AuthenticatedUser } from "src/definitions/auth";
import type { Fetch } from "src/definitions/fetch";
import type { Organization } from "src/definitions/organization";
import { getApiUrl, makeApiRequestOrFail } from "../fetch";

type DatapassUserPayload = {
  siret: string;
  email: string;
};

type CreateDatapassUser = (opts: {
  fetch: Fetch;
  token: string;
  data: DatapassUserPayload;
}) => Promise<AuthenticatedUser>;

export const createDatapassUser: CreateDatapassUser = async ({
  fetch,
  token,
  data: { siret, email },
}) => {
  const body = JSON.stringify({ organization_siret: siret, email });
  const url = `${getApiUrl()}/auth/datapass/users`;
  const request = new Request(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Signed-Token": token },
    body,
  });

  const response = await makeApiRequestOrFail(fetch, request);

  const data = await response.json();

  const authenticatedUser: AuthenticatedUser = {
    account: {
      organizationSiret: data.organization_siret,
      role: data.role,
      email: data.email,
    },
    apiToken: data.api_token,
  };
  return authenticatedUser;
};

type DatapassUserInfo = {
  organizations: Organization[];
  email: string;
};

type DatapassUserData = {
  token: string;
  info: DatapassUserInfo;
};

export const getDatapassUserInfoFromURLSearchParams = (
  searchParams: URLSearchParams
): DatapassUserData => {
  const infoString = searchParams.get("info");
  const token = searchParams.get("token");

  if (!infoString || !token) {
    throw new Error("no info or token found ");
  }

  const info = JSON.parse(infoString) as DatapassUserInfo;
  return {
    token,
    info,
  };
};
