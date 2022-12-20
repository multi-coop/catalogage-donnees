import type { Organization } from "src/definitions/organization";
import { range } from "$lib/util/array";
import { randint } from "src/lib/util/random";

export const getFakeSiret = (): string => {
  return range(14)
    .map(() => randint(0, 10).toString())
    .join("");
};

export const getFakeOrganization = (
  obj: Partial<Organization> = {}
): Organization => {
  return {
    name: obj.name || "Test org",
    siret: obj.siret || getFakeSiret(),
  };
};
