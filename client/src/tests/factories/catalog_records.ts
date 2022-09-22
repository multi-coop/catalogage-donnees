import type { CatalogRecord } from "src/definitions/catalog_records";
import { getFakeOrganization } from "./organizations";

export const getFakeCatalogRecord = (
  obj: Partial<CatalogRecord> = {}
): CatalogRecord => {
  return {
    createdAt: obj.createdAt || new Date(),
    organization: obj.organization || getFakeOrganization(),
  };
};
