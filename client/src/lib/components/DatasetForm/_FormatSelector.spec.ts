/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";
import { fireEvent, render } from "@testing-library/svelte";
import type { DataFormat } from "src/definitions/dataformat";
import FormatSelector from "./_FormatSelector.svelte";

const formatOptions: DataFormat[] = [
  {
    name: "label-1",
    id: 1,
  },
  {
    name: "label-2",
    id: 2,
  },
  {
    name: "label-3",
    id: 3,
  },
];

describe("Test the select component", () => {
  test("should display a select input with 3 options", () => {
    const props = {
      formatOptions,
    };

    const { getAllByRole } = render(FormatSelector, { props });

    expect(getAllByRole("listbox").length).toBe(1);
  });

  test("should display a select input with 3 options after start to type", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "label",
      },
    });
    expect(getAllByRole("option").length).toBe(3);
  });

  test("should display a select input with 3 options after  hitting  alt + down arrow", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
      altKey: true,
    });
    expect(getAllByRole("option").length).toBe(3);
  });

  test("should display a select input with 3 options after  start typing and hitting down arrow key", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "label",
      },
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });
    expect(getAllByRole("option").length).toBe(3);
  });

  test("should display a select input with 3 options after  start typing and hitting down arrow key", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, queryByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "label",
      },
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "Escape",
    });
    expect(queryByRole("option")).toBe(null);
  });

  test("should select an option after hitting Enter", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "lab",
      },
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "Enter",
    });

    const tags = getAllByRole("listitem");

    expect(tags).toHaveLength(1);

    expect(tags[0]).toHaveTextContent("label-1", {
      normalizeWhitespace: true,
    });

    expect(combobox).toHaveValue("");

    expect(combobox).toHaveValue("");
  });

  test("should select the second option after hitting down arrow twice and Enter", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "lab",
      },
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "Enter",
    });
    const tags = getAllByRole("listitem");

    expect(tags).toHaveLength(1);

    expect(tags[0]).toHaveTextContent("label-2", {
      normalizeWhitespace: true,
    });

    expect(combobox).toHaveValue("");
  });

  test("should select the second option after hitting down arrow 3 times and Enter", async () => {
    const props = {
      formatOptions,
    };

    const { getByRole, getAllByRole } = render(FormatSelector, { props });

    const combobox = getByRole("combobox");

    await fireEvent.input(combobox, {
      target: {
        value: "label-2",
      },
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "Enter",
    });

    const tags = getAllByRole("listitem");

    expect(tags).toHaveLength(1);

    expect(tags[0]).toHaveTextContent("label-2", {
      normalizeWhitespace: true,
    });

    expect(combobox).toHaveValue("");
  });
});
