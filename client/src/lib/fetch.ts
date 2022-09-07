import { browser } from "$app/env";
import { API_BROWSER_URL, API_SSR_URL } from "src/env";
import type { Fetch } from "src/definitions/fetch";
import type { Maybe } from "./util/maybe";
import { pushApiError } from "./stores/errors";

/**
 * Return the base API URL to be used for `fetch()` requests by the client.
 *
 * Example usage:
 * ```
 * const url = `${getApiUrl()}/some/resource/`;
 * const response = await fetch(url);
 * ```
 */
export const getApiUrl = (): string => {
  if (browser) {
    // This is:
    // * http://localhost:3579 on local.
    // * /api when live (sends requests to Nginx, which serves the frontend app).
    return API_BROWSER_URL;
  }
  // This is always http://localhost:3579.
  // In live environments (prod/staging/etc), this ensures we don't travel the Internet
  // when making requests during SSR (Server-Side Rendering).
  return API_SSR_URL;
};

export const maybePatchDataUrl = async (
  response: Response,
  requestUrl: URL
): Promise<Response> => {
  /**
   * NOTE: What's with all this?
   *
   * When using `load`, SvelteKit has a technique called _hydration_ to send data
   * fetched during SSR to the browser.
   * See: https://kit.svelte.dev/docs/appendix#hydration
   *
   * It is fairly easy for this technique to fail, which typically results in duplicated requests
   * to the API server. SvelteKit can't warn us about it yet.
   * See also: https://github.com/sveltejs/kit/issues/3729
   *
   * One key thing for hydration to work is that the `data-url` of the special
   * HTML tag included in the SSR HTML should match the URL of a request the browser
   * might do once it loads the app.
   *
   * As per our API-client wiring strategy (see `getApiUrl()` above), this is _generally_ the case.
   * But in some situations these URLs may be different (1), e.g. because in live environments
   * SSR and browser API calls are made to different locations.
   *
   * So right now we need this patch (2) to ensure `data-url` values match in that case too.
   *
   * See: https://github.com/etalab/catalogage-donnees/issues/71
   */

  // (1)
  const shouldPatchDataUrl = API_SSR_URL !== API_BROWSER_URL;

  if (!shouldPatchDataUrl) {
    return response;
  }

  if (!response.body) {
    return response;
  }

  // (2)
  const ssrDataUrl = API_SSR_URL;
  const browserDataUrl = ensureHasOrigin(
    `http://${requestUrl.host}`,
    API_BROWSER_URL
  );
  const body = await response.text();
  const patchedBody = body.replace(
    `data-url="${ssrDataUrl}`,
    `data-url="${browserDataUrl}`
  );

  return new Response(patchedBody, response);
};

const ensureHasOrigin = (origin: string, value: string) => {
  const isPath = value.startsWith("/");
  if (isPath) {
    return `${origin}${value}`;
  }
  return value;
};

export const getHeaders = (apiToken?: string): [string, string][] => {
  return apiToken ? [["authorization", `Bearer ${apiToken}`]] : [];
};

export async function makeApiRequest(
  fetch: Fetch,
  request: Request
): Promise<Maybe<Response>> {
  const response = await fetch(request);

  if (response.status >= 400) {
    pushApiError(response);
    return null;
  }

  return response;
}

export async function makeApiRequestOrFail(
  fetch: Fetch,
  request: Request
): Promise<Maybe<Response>> {
  const response = await fetch(request);

  if (!response.ok) {
    pushApiError(response);
    return Promise.reject(response);
  }
  return response;
}
