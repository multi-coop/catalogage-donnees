import type { Fetch } from "src/definitions/fetch";
import { getApiUrl } from "../fetch";

type DatapassUserPayload = {
  siret: string;
  email: string;
  token: string;
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
  data: DatapassUserPayload;
}) => Promise<CreatedDatapassUserResponse>;

export const createDatapassUser: CreateDatapassUser = async ({
  fetch,
  data: { siret, email, token },
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
