import type { ExtraFieldValue } from "src/definitions/catalogs";
import type {
  ActiveDatasetFiltersMap,
  BasicMap,
  DatasetFiltersInfo,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import type { ExtraField } from "src/definitions/extraField";

const getExtraFieldValuesFiltersMap = (
  extraFields: ExtraField[],
  extraFieldValues: ExtraFieldValue[]
): BasicMap[] => {
  return extraFieldValues.reduce((prev, next) => {
    const foundExtraField = extraFields.find(
      (item) => item.id === next.extraFieldId
    );

    if (!foundExtraField) {
      return prev;
    }
    return [
      ...prev,
      {
        id: foundExtraField.id,
        key: foundExtraField.title,
        value: next.value,
      },
    ];
  }, [] as BasicMap[]);
};

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
    extraFieldValues: filtersValue.extraFieldValues
      ? getExtraFieldValuesFiltersMap(
          filtersInfo.extraFields,
          filtersValue.extraFieldValues
        )
      : undefined,
  };
};

export const getActiveFiltersCount = (map: ActiveDatasetFiltersMap): number => {
  return Object.entries(map).reduce((prev, next) => {
    if (!next[1]) {
      return prev;
    }
    if (Array.isArray(next[1])) {
      return next[1].length + prev;
    }
    return 1 + prev;
  }, 0);
};

export const removeNonExistingFiltersValue = (
  filtersValues: DatasetFiltersValue
): DatasetFiltersValue => {
  return Object.entries(filtersValues).reduce((prev, next) => {
    if (next[1]) {
      return { ...prev, [next[0]]: next[1] };
    }

    return prev;
  }, {} as DatasetFiltersValue);
};
