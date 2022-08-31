export type ExtraFieldType = "TEXT" | "ENUM" | "BOOL";

export interface Catalog {
  organizationSiret: string;
  extraFields: ExtraField<ExtraFieldType>[];
}

type ExtraFieldData<T> = T extends "TEXT"
  ? Record<string, never>
  : T extends "ENUM"
  ? { values: string[] }
  : T extends "BOOL"
  ? { trueValue: string; falseValue: string }
  : never;

export interface ExtraField<T extends ExtraFieldType = ExtraFieldType> {
  id: string;
  name: string;
  title: string;
  hintText: string;
  type: T;
  data: ExtraFieldData<T>;
}

export interface ExtraFieldValue {
  extraFieldId: string;
  value: string;
}
