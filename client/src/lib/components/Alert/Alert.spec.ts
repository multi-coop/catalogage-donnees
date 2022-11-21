/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import Alert from "./Alert.svelte";

describe("Test the dataset list", () => {
  test("The list has the expected number of items", () => {
    const { getByRole } = render(Alert, {
      props: {
        title: "Attention : titre du message",
        description: "une jolie description",
      },
    });
    expect(getByRole("heading")).toHaveTextContent(
      "Attention : titre du message"
    );
  });
});
