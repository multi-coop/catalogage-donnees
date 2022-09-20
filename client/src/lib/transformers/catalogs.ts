import type { Catalog, ExtraField } from "src/definitions/catalogs";

const toExtraField = (data: any): ExtraField => {
  const { hint_text, ...rest } = data;

  let { data: fieldData } = data;

  if (data.type === "BOOL") {
    fieldData = {
      trueValue: fieldData.true_value,
      falseValue: fieldData.false_value,
    };
  }

  return {
    ...rest,
    hintText: hint_text,
    data: fieldData,
  };
};

export const toCatalog = (data: any): Catalog => {
  const { organization, extra_fields } = data;
  return {
    organization,
    extraFields: extra_fields.map((v: any) => toExtraField(v)),
  };
};
