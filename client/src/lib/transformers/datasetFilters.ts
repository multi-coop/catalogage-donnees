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
    format_id,
    ...rest
  } = data;
  return {
    organizationSiret: organization_siret,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    tagId: tag_id,
    formatId: format_id,
    ...rest,
  };
};

export const toFiltersValue = (
  searchParams: URLSearchParams
): DatasetFiltersValue => {
  const formatId = searchParams.get("format_id");
  return {
    organizationSiret: searchParams.get("organization_siret"),
    geographicalCoverage: searchParams.get("geographical_coverage"),
    service: searchParams.get("service"),
    formatId: formatId ? parseInt(formatId) : null,
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
    formatId,
    technicalSource,
    tagId,
    license,
  } = value;

  return [
    ["organization_siret", organizationSiret],
    ["geographical_coverage", geographicalCoverage],
    ["service", service],
    ["format_id", formatId],
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
): { [K in keyof DatasetFiltersValue]: Maybe<string> } => {
  return {
    organizationSiret: Maybe.map(
      value.organizationSiret,
      (v) => organizationSiretToName[v]
    ),
    geographicalCoverage: value.geographicalCoverage,
    service: value.service,
    formatId: Maybe.map(value.formatId, (v) => formatIdToName[v]),
    technicalSource: value.technicalSource,
    tagId: Maybe.map(value.tagId, (v) => tagIdToName[v]),
    license: Maybe.map(value.license, (v) =>
      v === "*" ? "Toutes les licences" : v
    ),
  };
};
