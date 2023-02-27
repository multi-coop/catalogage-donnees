/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import type { ExtraField } from "src/definitions/extraField";

import ExtraFieldComponent from "./_ExtraField.svelte";

describe("Extra field", () => {
  test("Should display an input for TEXT extra field", () => {
    const extraField: ExtraField = {
      id: "<id>",
      name: "referentiel",
      title: "Référentiel",
      hintText: "Quel est le référentiel ?",
      type: "TEXT",
      data: {},
    };
    const { getByRole } = render(ExtraFieldComponent, { extraField });
    const input = getByRole("textbox", { name: /Référentiel/i });
    expect(input).toBeInTheDocument();
  });

  test("Should display a radio group for BOOL extra field", () => {
    const extraField: ExtraField = {
      id: "<id>",
      name: "donnees_pi",
      title: "Données PI",
      hintText: "Ces données relèvent-elles d'une propriété intellectuelle ?",
      type: "BOOL",
      data: {
        trueValue: "Oui, bien sûr",
        falseValue: "Non, absolument pas",
      },
    };
    const { getByRole, getAllByRole } = render(ExtraFieldComponent, {
      extraField,
    });
    const group = getByRole("radiogroup", { name: /Données PI/i });
    expect(group).toBeInTheDocument();
    const options = getAllByRole("radio") as HTMLInputElement[];
    expect(options.length).toBe(2);
    expect(options[0].value).toBe("Oui, bien sûr");
    expect(options[1].value).toBe("Non, absolument pas");
  });

  test("Should display a select for ENUM extra field", () => {
    const extraField: ExtraField = {
      id: "<id>",
      name: "referentiel",
      title: "Référentiel",
      hintText: "Quel est le référentiel ?",
      type: "ENUM",
      data: {
        values: ["Référentiel A", "Référentiel B", "Référentiel C"],
      },
    };
    const { getAllByRole, getByRole } = render(ExtraFieldComponent, {
      extraField,
    });
    const select = getByRole("combobox", { name: /Référentiel/i });
    expect(select).toBeInTheDocument();
    const options = getAllByRole("option") as HTMLOptionElement[];
    expect(options.length).toBe(4);
    expect(options[0]).toBeDisabled();
    expect(options.slice(1).map((opt) => opt.value)).toEqual([
      "Référentiel A",
      "Référentiel B",
      "Référentiel C",
    ]);
  });

  test("Renders Markdown hint texts as HTML", () => {
    const extraField: ExtraField = {
      id: "<id>",
      name: "referentiel",
      title: "Référentiel",
      hintText:
        "**Important** : indiquez un référentiel ([exemples](https://example.org))",
      type: "TEXT",
      data: {},
    };
    const { getByRole } = render(ExtraFieldComponent, { extraField });
    const link = getByRole("link", { name: /exemples/i });
    expect(link).toBeInTheDocument();
  });
});
