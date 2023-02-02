/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";
import { fireEvent, render } from "@testing-library/svelte";
import type { SelectOption } from "src/definitions/form";
import SearcheableComboBox from "./SearcheableComboBox.svelte";

const options: SelectOption<number>[] = [
  {
    label: "label-1",
    value: 1,
  },
  {
    label: "label-2",
    value: 2,
  },
  {
    label: "label-3",
    value: 3,
  },
];

describe("Test the select component", () => {
  test("should display a select input with 3 options", () => {
    const props = {
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getAllByRole } = render(SearcheableComboBox, { props });

    expect(getAllByRole("listbox").length).toBe(1);
  });

  test("should display a select input with 3 options after start to type", async () => {
    const props = {
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole, getAllByRole } = render(SearcheableComboBox, { props });

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
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole, getAllByRole } = render(SearcheableComboBox, { props });

    const combobox = getByRole("combobox");

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
      altKey: true,
    });
    expect(getAllByRole("option").length).toBe(3);
  });

  test("should display a select input with 3 options after  start typing and hitting down arrow key", async () => {
    const props = {
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole, getAllByRole } = render(SearcheableComboBox, { props });

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
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole, queryByRole } = render(SearcheableComboBox, { props });

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
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole } = render(SearcheableComboBox, { props });

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

    expect(combobox).toHaveValue("label-1");
  });

  test("should select the second option after hitting down arrow twice and Enter", async () => {
    const props = {
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole } = render(SearcheableComboBox, { props });

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

    expect(combobox).toHaveValue("label-2");
  });

  test("should select the second option after hitting down arrow 3 times and Enter", async () => {
    const props = {
      options,
      label: "My Nice Select",
      name: "mySelect",
      hintText: "my nice hint text",
    };

    const { getByRole } = render(SearcheableComboBox, { props });

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
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "ArrowDown",
    });

    await fireEvent.keyDown(combobox, {
      key: "Enter",
    });

    expect(combobox).toHaveValue("label-1");
  });
});
