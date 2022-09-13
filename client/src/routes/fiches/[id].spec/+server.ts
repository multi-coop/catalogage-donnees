
// @migration task: Check imports
/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import index from "./index.svelte";
import { getFakeDataset } from "src/tests/factories/dataset";

const dataset = getFakeDataset({
  id: "d4765f06-ccdf-4bae-b237-2bced67e6dc2",
  title: "foo",
  description: "bar baz crux",
  formats: ["other"],
  producerEmail: "service@mydomain.org",
  contactEmails: ["service@mydomain.org"],
});

describe("Dataset detail page header", () => {
  test("The dataset title is present", () => {
    const { getByRole } = render(index, { dataset });
    expect(getByRole("heading", { level: 1 })).toHaveTextContent(dataset.title);
  });
});

describe("Dataset detail page action buttons", () => {
  test("The button to modify the dataset is present", () => {
    const { getByText } = render(index, { dataset });
    const modifyButton = getByText("Modifier");
    expect(modifyButton).toBeInTheDocument();
    expect(modifyButton.getAttribute("href")).toContain(dataset.id);
  });
  test("The button to contact the author is present", () => {
    const { getByText } = render(index, { dataset });
    const contactButton = getByText("Contacter le producteur");
    expect(contactButton).toBeInTheDocument();
    expect(contactButton.getAttribute("href")).toContain(dataset.producerEmail);
  });
});

describe("Dataset detail description", () => {
  test("The description is shown", async () => {
    const { getByTestId } = render(index, { dataset });
    const description = getByTestId("dataset-description");
    expect(description).toHaveTextContent(dataset.description);
  });

  test("The url link button is present if a url is set", async () => {
    const { getByText, queryByText, rerender } = render(index, {
      dataset: { ...dataset, url: null },
    });
    let urlLink = queryByText("Voir les données", { exact: false });
    expect(urlLink).not.toBeInTheDocument();
    rerender({
      props: { dataset: { ...dataset, url: "https://example.org" } },
    });
    urlLink = getByText("Voir les données", { exact: false });
    expect(urlLink).toBeInTheDocument();
    expect(urlLink).toHaveAttribute("href", "https://example.org");
  });

  test("The license is shown if it is set", async () => {
    const { getByText, queryByText, rerender } = render(index, {
      dataset: { ...dataset, license: null },
    });
    let license = queryByText("Licence Ouverte", { exact: false });
    expect(license).not.toBeInTheDocument();
    rerender({
      props: { dataset: { ...dataset, license: "Licence Ouverte" } },
    });
    license = getByText("Licence Ouverte", { exact: false });
    expect(license).toBeInTheDocument();
  });
});
