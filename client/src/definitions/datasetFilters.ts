import type { ExtraFieldValue } from "./catalogs";
import type { DataFormat } from "./dataformat";
import type { ExtraField } from "./extraField";
import type { SelectOption } from "./form";
import type { Organization } from "./organization";
import type { Tag } from "./tag";

export type DatasetFiltersInfo = {
  organizationSiret: Organization[];
  geographicalCoverage: string[];
  service: string[];
  formatId: DataFormat[];
  technicalSource: string[];
  tagId: Tag[];
  license: string[];
  extraFields: ExtraField[];
};

export type DatasetFiltersValue = {
  organizationSiret?: string;
  geographicalCoverage?: string;
  service?: string;
  formatId?: number;
  technicalSource?: string;
  tagId?: string;
  license?: string;
  extraFieldValues?: ExtraFieldValue[];
};

type BasicMap = {
  key: string;
  value: string | number;
};

export type ActiveDatasetFiltersMap = {
  organizationSiret?: BasicMap;
  geographicalCoverage?: BasicMap;
  service?: BasicMap;
  formatId?: BasicMap;
  technicalSource?: BasicMap;
  tagId?: BasicMap;
  license?: BasicMap;
  extraFieldValues?: BasicMap;
};

export type DatasetFiltersOptions = {
  [K in keyof Omit<DatasetFiltersValue, "extraFieldValues">]: SelectOption<
    DatasetFiltersValue[K]
  >[];
};
