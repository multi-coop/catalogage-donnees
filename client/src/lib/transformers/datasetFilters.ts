import type { ExtraFieldValue } from "src/definitions/catalogs";
import type {
  DatasetFiltersInfo,
  DatasetFiltersOptions,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import type { BoolExtraField, ExtraField } from "src/definitions/extraField";
import type { QueryParamRecord } from "src/definitions/url";
import { Maybe } from "../util/maybe";

export const transformRawExtraFieldToBoolExtraField = (
  rawExtraField: any
): BoolExtraField => {
  return {
    hintText: rawExtraField.hintText,
    name: rawExtraField.name,
    title: rawExtraField.title,
    type: rawExtraField.type,
    id: rawExtraField.id,
    data: {
      trueValue: rawExtraField.data.true_value,
      falseValue: rawExtraField.data.false_value,
    },
  };
};

const transformExtraFieldValueToAPIQueryParam = (
  extraFieldValue: ExtraFieldValue
): {
  value: string;
  extra_field_id: string;
} => {
  return {
    extra_field_id: extraFieldValue.extraFieldId,
    value: extraFieldValue.value,
  };
};

export const transformAPIQueryParamToExtraFieldValue = (value: {
  value: string;
  extra_field_id: string;
}): ExtraFieldValue => {
  return {
    extraFieldId: value.extra_field_id,
    value: value.value,
  };
};

export const tranformRawExtraField = (rawExtraField: any): ExtraField => {
  switch (rawExtraField.type) {
    case "BOOL":
      return transformRawExtraFieldToBoolExtraField(rawExtraField);

    default:
      return rawExtraField;
  }
};

export const toFiltersInfo = (data: any): DatasetFiltersInfo => {
  const {
    organization_siret,
    geographical_coverage,
    technical_source,
    tag_id,
    format_id,
    extra_fields,
    ...rest
  } = data;
  return {
    organizationSiret: organization_siret,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    tagId: tag_id,
    formatId: format_id,
    extraFields: extra_fields.map(tranformRawExtraField),
    ...rest,
  };
};

const getExtraFieldValues = (
  extraFieldValuesString: string | null
): ExtraFieldValue[] | null => {
  if (!extraFieldValuesString) {
    return null;
  }

  return JSON.parse(extraFieldValuesString).map(
    transformAPIQueryParamToExtraFieldValue
  );
};

const getExtraFieldValuesString = (
  extraFieldValues: ExtraFieldValue[] | null
): string | null => {
  if (!extraFieldValues) {
    return null;
  }

  return JSON.stringify(
    extraFieldValues.map(transformExtraFieldValueToAPIQueryParam)
  );
};

export const toFiltersValue = (
  searchParams: URLSearchParams
): DatasetFiltersValue => {
  const formatId = searchParams.get("format_id");

  const extraFieldValuesString = searchParams.get("extra_field_values");

  return {
    organizationSiret: searchParams.get("organization_siret"),
    geographicalCoverage: searchParams.get("geographical_coverage"),
    service: searchParams.get("service"),
    formatId: formatId ? parseInt(formatId) : null,
    technicalSource: searchParams.get("technical_source"),
    tagId: searchParams.get("tag_id"),
    license: searchParams.get("license"),
    extraFieldValues: getExtraFieldValues(extraFieldValuesString),
  };
};

export const toFiltersParams = (
  value: DatasetFiltersValue
): QueryParamRecord => {
  const {
    organizationSiret,
    geographicalCoverage,
    service,
    formatId,
    technicalSource,
    tagId,
    license,
    extraFieldValues,
  } = value;

  return [
    ["organization_siret", organizationSiret],
    ["geographical_coverage", geographicalCoverage],
    ["service", service],
    ["format_id", formatId],
    ["technical_source", technicalSource],
    ["tag_id", tagId],
    ["license", license],
    ["extra_field_values", getExtraFieldValuesString(extraFieldValues)],
  ];
};

export const toFiltersOptions = (
  info: DatasetFiltersInfo
): DatasetFiltersOptions => {
  return {
    organizationSiret: info.organizationSiret.map(({ name, siret }) => ({
      label: name,
      value: siret,
    })),
    geographicalCoverage: info.geographicalCoverage.map((value) => ({
      label: value,
      value,
    })),
    service: info.service.map((value) => ({ label: value, value })),
    formatId: info.formatId.map((dataformat) => ({
      label: dataformat.name,
      value: dataformat.id,
    })),
    technicalSource: info.technicalSource.map((value) => ({
      label: value,
      value,
    })),
    tagId: info.tagId.map((tag) => ({ label: tag.name, value: tag.id })),
    license: info.license.map((value) => ({
      label: value === "*" ? "Toutes les licences" : value,
      value,
    })),
  };
};

export const toFiltersButtonTexts = (
  value: DatasetFiltersValue,
  organizationSiretToName: Record<string, string>,
  tagIdToName: Record<string, string>,
  formatIdToName: Record<string, string>
): {
  [K in keyof Omit<DatasetFiltersValue, "extraFieldValues">]: Maybe<string>;
} => {
  return {
    organizationSiret: Maybe.map(
      value.organizationSiret,
      (v) => organizationSiretToName[v]
    ),
    geographicalCoverage: value.geographicalCoverage,
    service: value.service,
    formatId: Maybe.map(value.formatId, (v) => formatIdToName[v]),
    tagId: Maybe.map(value.tagId, (v) => tagIdToName[v]),
    technicalSource: value.technicalSource,
    license: Maybe.map(value.license, (v) =>
      v === "*" ? "Toutes les licences" : v
    ),
  };
};
