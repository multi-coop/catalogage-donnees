import type { ExtraField } from "./extraField";
import type { Organization } from "./organization";

export type Catalog = {
  organization: Organization;
  extraFields: ExtraField[];
}
export interface ExtraFieldValue {
  extraFieldId: string;
  value: string;
}
