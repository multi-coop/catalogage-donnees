type ExtraFieldBase = {
  id: string;
  name: string;
  title: string;
  hintText: string;
};

type TextExtraField = {
  type: "TEXT";
  data: Record<string, never>;
} & ExtraFieldBase;

export type BoolExtraField = {
  type: "BOOL";
  data: {
    trueValue: string;
    falseValue: string;
  };
} & ExtraFieldBase;

type EnumExtraField = {
  type: "ENUM";
  data: {
    values: string[];
  };
} & ExtraFieldBase;

export type ExtraField = TextExtraField | BoolExtraField | EnumExtraField;
