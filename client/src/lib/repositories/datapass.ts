import { SearchParamsValidationError } from "src/definitions/errors";
import type { Fetch } from "src/definitions/fetch";
import type { Organization } from "src/definitions/organization";
import { getApiUrl } from "../fetch";

type DatapassUserPayload = {
  siret: string;
  email: string;
};

type CreatedDatapassUserResponse = {
  id: string;
  siret: string;
  email: string;
  role: string;
  apiToken: string;
};

type CreateDatapassUser = (opts: {
  fetch: Fetch;
  token: string;
  data: DatapassUserPayload;
}) => Promise<CreatedDatapassUserResponse>;

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

  const response = await fetch(request);

  if (!response.ok) {
    throw new Error("unable to create the datapass user");
  }

  const data = await response.json();

  return {
    apiToken: data.api_token,
    siret: data.organization_siret,
    role: data.role,
    email: data.email,
    id: data.id,
  };
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
    throw new SearchParamsValidationError("no info or token found ");
  }

  const info = JSON.parse(infoString) as DatapassUserInfo;

  if (!info.email || !info.organizations || info.organizations.length === 0) {
    throw new SearchParamsValidationError("some informations are missing");
  }
  return {
    token,
    info,
  };
};
