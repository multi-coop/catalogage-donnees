import type { BoolExtraField } from "src/definitions/extraField";
import type { SelectOption } from "src/definitions/form";

export const toSelectOption = (extraField: BoolExtraField): SelectOption[] => {
  return [
    {
      label: extraField.data.trueValue,
      value: extraField.data.trueValue,
    },
    {
      label: extraField.data.falseValue,
      value: extraField.data.falseValue,
    },
  ];
};
