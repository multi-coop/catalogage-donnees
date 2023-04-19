import type {
  ActiveDatasetFiltersMap,
  DatasetFiltersInfo,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import { getFakeOrganization } from "src/tests/factories/organizations";
import { buildFakeTag } from "src/tests/factories/tags";
import { buildActiveFiltersMap, getActiveFiltersCount } from "./datasetFilters";

test("buildActiveFiltersMap", () => {
  const filtersInfos: DatasetFiltersInfo = {
    organizationSiret: [
      getFakeOrganization({
        siret: "1234",
        name: "myorganization",
      }),
      getFakeOrganization(),
    ],
    geographicalCoverage: ["oversea"],
    service: ["DGIFP"],
    formatId: [
      {
        name: "XLSX",
        id: 2,
      },
      {
        name: "CSV",
        id: 1,
      },
    ],
    technicalSource: ["ADEME"],
    tagId: [
      buildFakeTag({
        id: "122",
        name: "tata",
      }),
    ],
    extraFields: [],
    license: ["malicence", "AGPL"],
  };

  const filtersValue: DatasetFiltersValue = {
    organizationSiret: "1234",
    geographicalCoverage: "oversea",
    service: "DGIFP",
    formatId: 2,
    technicalSource: "ADEME",
    tagId: "122",
    license: "AGPL",
    extraFieldValues: null,
  };

  const expectedResult: ActiveDatasetFiltersMap = {
    organizationSiret: {
      key: "Catalogue",
      value: "myorganization",
    },
    geographicalCoverage: {
      key: "Couverture géopgraphique",
      value: "oversea",
    },
    service: {
      key: "Service Producteur de la donnée",
      value: "DGIFP",
    },
    formatId: {
      key: "Format de mise à disposition",
      value: "XLSX",
    },
    technicalSource: {
      key: "Système d’information source",
      value: "ADEME",
    },
    tagId: {
      key: "Mot-clé",
      value: "tata",
    },
    license: {
      key: "Licence",
      value: "AGPL",
    },
  };

  const result = buildActiveFiltersMap(filtersInfos, filtersValue);

  expect(expectedResult).toEqual(result);
});

test("getActiveFiltersMap", () => {
  const map: ActiveDatasetFiltersMap = {
    organizationSiret: {
      key: "Catalogue",
      value: "myorganization",
    },
    geographicalCoverage: {
      key: "Couverture géopgraphique",
      value: "oversea",
    },
    service: {
      key: "Service Producteur de la donnée",
      value: "DGIFP",
    },
  };

  const result = getActiveFiltersCount(map);

  expect(result).toEqual(3);
});
