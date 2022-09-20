/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import TextOrHtml from "./TextOrHtml.svelte";

describe("TextOrHtml", () => {
  test("Should display text", () => {
    const { getByText } = render(TextOrHtml, { value: "String" });
    expect(getByText("String")).toBeInTheDocument();
  });

  test("Should escape content marked as HTML", () => {
    const { getByText, queryByRole } = render(TextOrHtml, {
      value: 'Visit <a href="...">me</a>',
    });
    expect(getByText('Visit <a href="...">me</a>')).toBeInTheDocument();
    expect(queryByRole("link")).toBeNull();
  });

  test("Should render content marked as HTML", () => {
    const { getByRole } = render(TextOrHtml, {
      value: { isHtml: true, content: 'Visit <a href="...">me</a>' },
    });
    const link = getByRole("link");
    expect(link).toBeInTheDocument();
  });
});
