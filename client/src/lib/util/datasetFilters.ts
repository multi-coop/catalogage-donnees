import type {
  ActiveDatasetFiltersMap,
  DatasetFiltersInfo,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";

export const buildActiveFiltersMap = (
  filtersInfo: DatasetFiltersInfo,
  filtersValue: DatasetFiltersValue
): ActiveDatasetFiltersMap => {
  const foundOrganization = filtersInfo.organizationSiret.find(
    (item) => item.siret === filtersValue.organizationSiret
  );
  const foundFormat = filtersInfo.formatId.find(
    (item) => item.id === filtersValue.formatId
  );
  const foundTag = filtersInfo.tagId.find(
    (item) => item.id === filtersValue.tagId
  );
  return {
    organizationSiret: foundOrganization
      ? {
          key: "Catalogue",
          value: foundOrganization?.name,
        }
      : undefined,
    geographicalCoverage: filtersValue.geographicalCoverage
      ? {
          key: "Couverture géopgraphique",
          value: filtersValue.geographicalCoverage,
        }
      : undefined,
    service: filtersValue.service
      ? {
          key: "Service Producteur de la donnée",
          value: filtersValue.service,
        }
      : undefined,
    formatId: foundFormat
      ? {
          key: "Format de mise à disposition",
          value: foundFormat?.name,
        }
      : undefined,
    technicalSource: filtersValue.technicalSource
      ? {
          key: "Système d’information source",
          value: filtersValue.technicalSource,
        }
      : undefined,
    tagId: foundTag
      ? {
          key: "Mot-clé",
          value: foundTag?.name,
        }
      : undefined,
    license: filtersValue.license
      ? {
          key: "Licence",
          value: filtersValue.license,
        }
      : undefined,
  };
};

export const getActiveFiltersCount = (map: ActiveDatasetFiltersMap): number =>
  Object.entries(map).reduce((prev, next) => (next[1] ? prev + 1 : prev), 0);
