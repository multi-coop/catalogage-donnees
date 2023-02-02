import type { DataFormat } from "src/definitions/dataformat";
import type { SelectOption } from "src/definitions/form";

import type { Tag } from "src/definitions/tag";
import type { TrustedHtml } from "../util/html";

export type LabelMap = { [key: string]: string | TrustedHtml };

export const toSelectOptions = (
  labelsMap: LabelMap
): Array<SelectOption<TrustedHtml | string>> => {
  const keys = Object.keys(labelsMap);

  const map = keys.map((key) => ({
    label: labelsMap[key],
    value: key,
  }));

  return map as Array<SelectOption<TrustedHtml | string>>;
};

export const transformTagToSelectOption = (tag: Tag): SelectOption => ({
  label: tag.name,
  value: `${tag.id}`,
});

export const transformDataFormatToSelectOption = (
  dataformat: DataFormat
): SelectOption<number> => ({
  label: dataformat.name,
  value: dataformat.id,
});

export const transoformSelectOptionToDataFormat = (
  selectOption: SelectOption<number>
): DataFormat => ({
  name: selectOption.label,
  id: selectOption.value,
});
