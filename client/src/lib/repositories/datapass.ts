import type { Fetch } from "src/definitions/fetch";
import { getApiUrl } from "../fetch";

type DatapassUserPayload = {
  siret: string;
  email: string;
  token: string;
};

type CreateDatapassUser = (opts: {
  fetch: Fetch;
  data: DatapassUserPayload;
}) => Promise<void>;

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
};
