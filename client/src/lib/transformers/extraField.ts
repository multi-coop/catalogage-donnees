import type {
  BoolExtraField,
  EnumExtraField,
} from "src/definitions/extraField";
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

export const transformEnumExtraFieldToSelectOptoon = (
  extraField: EnumExtraField
): SelectOption[] => {
  return extraField.data.values.map((item) => {
    return {
      label: item,
      value: item,
    };
  });
};
