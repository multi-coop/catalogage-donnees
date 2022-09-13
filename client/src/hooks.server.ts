import type { Handle } from "@sveltejs/kit";
import { maybePatchDataUrl } from "$lib/fetch";

// See: https://kit.svelte.dev/docs/hooks#handle
export const handle: Handle = async ({ event, resolve }) => {
  let response = await resolve(event);

  response = await maybePatchDataUrl(response, event.url);

  return response;
};
