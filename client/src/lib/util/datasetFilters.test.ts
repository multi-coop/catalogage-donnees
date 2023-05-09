import type {
  ActiveDatasetFiltersMap,
  DatasetFiltersInfo,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import { getFakeOrganization } from "src/tests/factories/organizations";
import { buildFakeTag } from "src/tests/factories/tags";
import { buildActiveFiltersMap, getActiveFiltersCount } from "./datasetFilters";
import type { ExtraFieldValue } from "src/definitions/catalogs";
import type {
  BoolExtraField,
  EnumExtraField,
} from "src/definitions/extraField";

test("buildActiveFiltersMap", () => {
  const extraField1: EnumExtraField = {
    id: "1234",
    name: "my name",
    title: "my title",
    hintText: "my-text",
    type: "ENUM",
    data: {
      values: ["my-extra-field"],
    },
  };

  const extraField2: BoolExtraField = {
    id: "4567",
    name: "my name",
    title: "my title",
    hintText: "my-text",
    type: "BOOL",
    data: {
      trueValue: "OUI",
      falseValue: "NON",
    },
  };
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
    extraFields: [extraField1, extraField2],
    license: ["malicence", "AGPL"],
  };

  const extraFieldValue1: ExtraFieldValue = {
    extraFieldId: "1234",
    value: "my-extra-field",
  };

  const extraFieldValue2: ExtraFieldValue = {
    extraFieldId: "4567",
    value: "Non",
  };

  const filtersValue: DatasetFiltersValue = {
    organizationSiret: "1234",
    geographicalCoverage: "oversea",
    service: "DGIFP",
    formatId: 2,
    technicalSource: "ADEME",
    tagId: "122",
    license: "AGPL",
    extraFieldValues: [extraFieldValue1, extraFieldValue2],
  };

  const expectedResult: ActiveDatasetFiltersMap = {
    organizationSiret: {
      key: "Catalogue",
      value: "myorganization",
    },
    geographicalCoverage: {
      key: "Couverture géographique",
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
    extraFieldValues: [
      {
        id: extraField1.id,
        key: extraField1.title,
        value: extraFieldValue1.value,
      },
      {
        id: extraField2.id,
        key: extraField2.title,
        value: extraFieldValue2.value,
      },
    ],
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
      key: "Couverture géographique",
      value: "oversea",
    },
    service: {
      key: "Service Producteur de la donnée",
      value: "DGIFP",
    },
    extraFieldValues: [
      {
        key: "my extra field",
        value: 66,
      },
      {
        key: "myExtra field 2",
        value: "67",
      },
    ],
  };

  const result = getActiveFiltersCount(map);

  expect(result).toEqual(5);
});
