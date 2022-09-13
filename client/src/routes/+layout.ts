import type { LayoutLoad.base } from "@sveltejs/kit";
import { authGuard } from "$lib/auth/guard";

export const load: LayoutLoad.base = async ({ url }) => {
  throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292693)");
  return authGuard(url);
};
