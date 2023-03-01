import type { Organization } from "./organization";

type ExtraFieldBase = {
  id: string;
  name: string;
  title: string;
  hintText: string;
};

type TextExtraField = {
  type: "TEXT";
  data: Record<string, never>;
} & ExtraFieldBase;

type BoolExtraField = {
  type: "BOOL";
  data: {
    trueValue: string;
    falseValue: string;
  };
} & ExtraFieldBase;

type EnumExtraField = {
  type: "ENUM";
  data: {
    values: string[];
  };
} & ExtraFieldBase;

export type ExtraField = TextExtraField | BoolExtraField | EnumExtraField;

export interface Catalog {
  organization: Organization;
  extraFields: ExtraField[];
}
export interface ExtraFieldValue {
  extraFieldId: string;
  value: string;
}
