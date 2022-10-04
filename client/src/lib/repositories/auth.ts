import type {
  PasswordLoginData,
  AuthenticatedUser,
  Account,
} from "src/definitions/auth";
import type { ApiResponse, Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequest } from "../fetch";
import { toAccount } from "../transformers/auth";
import { Maybe } from "../util/maybe";

type LoginWithPassword = (opts: {
  fetch: Fetch;
  data: PasswordLoginData;
}) => Promise<ApiResponse<AuthenticatedUser>>;

export const loginWithPassword: LoginWithPassword = async ({ fetch, data }) => {
  const body = JSON.stringify(data);
  const url = `${getApiUrl()}/auth/login/`;

  const request = new Request(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });

  const response = await fetch(request);

  const apiData = await response.json();

  return {
    status: response.status,
    data: {
      account: toAccount(apiData),
      apiToken: apiData.api_token,
    },
  };
};

type LoginWithDataPass = (opts: {
  params: URLSearchParams;
}) => Promise<Maybe<AuthenticatedUser>>;

export const loginWithDataPass: LoginWithDataPass = async ({ params }) => {
  const userInfo = params.get("user_info");

  if (!userInfo) {
    return null;
  }

  try {
    const data = JSON.parse(userInfo);
    return {
      account: toAccount(data),
      apiToken: data.api_token,
    };
  } catch (e) {
    return null;
  }
};

type GetMe = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Maybe<Account>>;

export const getMe: GetMe = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/auth/users/me/`;
  const request = new Request(url, { headers: getHeaders(apiToken) });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (resp) => {
    const data = await resp.json();
    return toAccount(data);
  });
};
