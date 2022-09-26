import { DATA_FORMAT_LABELS } from "src/constants";
import type {
  DatasetFiltersInfo,
  DatasetFiltersOptions,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import type { QueryParamRecord } from "src/definitions/url";
import { Maybe } from "../util/maybe";

export const toFiltersInfo = (data: any): DatasetFiltersInfo => {
  const {
    organization_siret,
    geographical_coverage,
    technical_source,
    tag_id,
    ...rest
  } = data;
  return {
    organizationSiret: organization_siret,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    tagId: tag_id,
    ...rest,
  };
};

export const toFiltersValue = (
  searchParams: URLSearchParams
): DatasetFiltersValue => {
  return {
    organizationSiret: searchParams.get("organization_siret"),
    geographicalCoverage: searchParams.get("geographical_coverage"),
    service: searchParams.get("service"),
    format: searchParams.get("format"),
    technicalSource: searchParams.get("technical_source"),
    tagId: searchParams.get("tag_id"),
    license: searchParams.get("license"),
  };
};

export const toFiltersParams = (
  value: DatasetFiltersValue
): QueryParamRecord => {
  const {
    organizationSiret,
    geographicalCoverage,
    service,
    format,
    technicalSource,
    tagId,
    license,
  } = value;

  return [
    ["organization_siret", organizationSiret],
    ["geographical_coverage", geographicalCoverage],
    ["service", service],
    ["format", format],
    ["technical_source", technicalSource],
    ["tag_id", tagId],
    ["license", license],
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
    format: info.format.map((value) => ({
      label: DATA_FORMAT_LABELS[value],
      value,
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
  tagIdToName: Record<string, string>
): { [K in keyof DatasetFiltersValue]: Maybe<string> } => {
  return {
    organizationSiret: Maybe.map(
      value.organizationSiret,
      (v) => organizationSiretToName[v]
    ),
    geographicalCoverage: value.geographicalCoverage,
    service: value.service,
    format: Maybe.map(value.format, (v) => DATA_FORMAT_LABELS[v]),
    technicalSource: value.technicalSource,
    tagId: Maybe.map(value.tagId, (v) => tagIdToName[v]),
    license: Maybe.map(value.license, (v) =>
      v === "*" ? "Toutes les licences" : v
    ),
  };
};
