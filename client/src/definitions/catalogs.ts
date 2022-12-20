import type { Organization } from "./organization";

interface ExtraFieldBase {
  id: string;
  name: string;
  title: string;
  hintText: string;
}

interface TextExtraField extends ExtraFieldBase {
  type: "TEXT";
  data: Record<string, never>;
}

interface BoolExtraField extends ExtraFieldBase {
  type: "BOOL";
  data: {
    trueValue: string;
    falseValue: string;
  };
}

interface EnumExtraField extends ExtraFieldBase {
  type: "ENUM";
  data: {
    values: string[];
  };
}

export type ExtraField = TextExtraField | BoolExtraField | EnumExtraField;

export interface Catalog {
  organization: Organization;
  extraFields: ExtraField[];
}
export interface ExtraFieldValue {
  extraFieldId: string;
  value: string;
}
