import type { Catalog, ExtraField } from "src/definitions/catalogs";

const toExtraField = (data: any): ExtraField => {
  const { hint_text, ...rest } = data;
  return {
    hintText: hint_text,
    ...rest,
  };
};

export const toCatalog = (data: any): Catalog => {
  const { organization_siret, extra_fields } = data;
  return {
    organizationSiret: organization_siret,
    extraFields: extra_fields.map((v: any) => toExtraField(v)),
  };
};
