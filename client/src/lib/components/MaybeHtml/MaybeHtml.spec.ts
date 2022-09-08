/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import MaybeHtml from "./MaybeHtml.svelte";

describe("MaybeHtml", () => {
  test("Should display string text", () => {
    const { getByText } = render(MaybeHtml, { text: "String" });
    expect(getByText("String")).toBeInTheDocument();
  });

  test("Should escape content marked as HTML", () => {
    const { getByText, queryByRole } = render(MaybeHtml, {
      text: 'Visit <a href="...">me</a>',
    });
    expect(getByText('Visit <a href="...">me</a>')).toBeInTheDocument();
    expect(queryByRole("link")).toBeNull();
  });

  test("Should render content marked as HTML", () => {
    const { getByRole } = render(MaybeHtml, {
      text: { isHTML: true, content: 'Visit <a href="...">me</a>' },
    });
    const link = getByRole("link");
    expect(link).toBeInTheDocument();
  });
});
