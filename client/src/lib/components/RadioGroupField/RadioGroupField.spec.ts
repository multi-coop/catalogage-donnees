/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import type { SelectOption } from "src/definitions/form";
import RadioGroupField from "./RadioGroupField.svelte";

describe("Radio group field", () => {
  const fruitOptions: SelectOption[] = [
    { value: "apple", label: "Apple" },
    { value: "orange", label: "Orange" },
    { value: "banana", label: "Banana" },
  ];

  const defaultProps = {
    name: "fruit",
    label: "Fruit",
    hintText: "Choose a fruit you would like",
    options: fruitOptions,
  };

  test("Should display a radio group with 3 options", () => {
    const { getByRole, getAllByRole } = render(RadioGroupField, defaultProps);
    const group = getByRole("radiogroup");
    expect(group).toBeInTheDocument();
    const options = getAllByRole("radio") as HTMLInputElement[];
    expect(options.length).toBe(3);
    expect(options.map((opt) => opt.value)).toEqual([
      "apple",
      "orange",
      "banana",
    ]);
  });

  test("Should mark option corresponding to given value as checked", () => {
    const props = { ...defaultProps, value: "apple" };
    const { getByRole, getAllByRole } = render(RadioGroupField, props);
    const group = getByRole("radiogroup");
    expect(group).toBeInTheDocument();
    const options = getAllByRole("radio") as HTMLInputElement[];
    expect(options.length).toBe(3);
    expect(options[0]).toBeChecked();
  });
});
