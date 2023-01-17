import type { DataFormat } from "./dataformat";
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
};

export type DatasetFiltersValue = {
  organizationSiret: string | null;
  geographicalCoverage: string | null;
  service: string | null;
  formatId: number | null;
  technicalSource: string | null;
  tagId: string | null;
  license: string | null;
};

export type DatasetFiltersOptions = {
  [K in keyof DatasetFiltersValue]: SelectOption<DatasetFiltersValue[K]>[];
};
