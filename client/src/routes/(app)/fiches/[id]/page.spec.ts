/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render } from "@testing-library/svelte";
import index from "./+page.svelte";
import { getFakeDataset } from "src/tests/factories/dataset";
import type {
  Catalog,
  ExtraField,
  ExtraFieldValue,
} from "src/definitions/catalogs";
import { login, logout } from "src/lib/stores/auth";
import { getFakeOrganization } from "src/tests/factories/organizations";
import { getFakeCatalogRecord } from "src/tests/factories/catalog_records";
import { getFakeAccount } from "src/tests/factories/accounts";

const organization = getFakeOrganization();

const catalog: Catalog = {
  organization,
  extraFields: [],
};

const dataset = getFakeDataset({
  id: "d4765f06-ccdf-4bae-b237-2bced67e6dc2",
  title: "foo",
  description: "bar baz crux",
  formats: [{ id: 55, name: "other" }],
  producerEmail: "service@mydomain.org",
  contactEmails: ["service@mydomain.org"],
  catalogRecord: getFakeCatalogRecord({
    organization,
  }),
});

const data = { catalog, dataset };

beforeAll(() =>
  login(getFakeAccount({ organizationSiret: organization.siret }), "abcd1234")
);

afterAll(() => logout());

describe("Dataset detail page header", () => {
  test("The dataset title is present", () => {
    const { getByRole } = render(index, { data });
    expect(getByRole("heading", { level: 1 })).toHaveTextContent(dataset.title);
  });
});

describe("Dataset detail page action buttons", () => {
  test("The button to modify the dataset is present", () => {
    const { getByText } = render(index, { data });
    const modifyButton = getByText("Modifier");
    expect(modifyButton).toBeInTheDocument();
    expect(modifyButton.getAttribute("href")).toContain(dataset.id);
  });
  test("The button to modify the dataset is absent if user does not belong to organization", async () => {
    login(getFakeAccount({ organizationSiret: "<other_siret>" }), "1234");
    const { queryByText } = render(index, { data });
    const modifyButton = queryByText("Modifier");
    expect(modifyButton).not.toBeInTheDocument();
  });
  test("The button to contact the author is present", () => {
    const { getByText } = render(index, { data });
    const contactButton = getByText("Contacter le producteur");
    expect(contactButton).toBeInTheDocument();
    expect(contactButton.getAttribute("href")).toContain(dataset.producerEmail);
  });
});

describe("Dataset detail description", () => {
  test("The description is shown", async () => {
    const { getByTestId } = render(index, { data });
    const description = getByTestId("dataset-description");
    expect(description).toHaveTextContent(dataset.description);
  });

  test("The url link button is present if a url is set", async () => {
    const { getByText, queryByText, rerender } = render(index, {
      data: { ...data, dataset: { ...dataset, url: null } },
    });
    let urlLink = queryByText("Voir les données", { exact: false });
    expect(urlLink).not.toBeInTheDocument();
    rerender({
      data: { ...data, dataset: { ...dataset, url: "https://example.org" } },
    });
    urlLink = getByText("Voir les données", { exact: false });
    expect(urlLink).toBeInTheDocument();
    expect(urlLink).toHaveAttribute("href", "https://example.org");
  });

  test("The license is shown if it is set", async () => {
    const { getByText, queryByText, rerender } = render(index, {
      data: { ...data, dataset: { ...dataset, license: null } },
    });
    let license = queryByText("Licence Ouverte", { exact: false });
    expect(license).not.toBeInTheDocument();

    rerender({
      data: { ...data, dataset: { ...dataset, license: "Licence Ouverte" } },
    });
    license = getByText("Licence Ouverte", { exact: false });
    expect(license).toBeInTheDocument();
  });
});

describe("Dataset detail extra fields", () => {
  test("Extra fields section not shown if no extra fields in catalog", () => {
    const { queryByRole } = render(index, { data });
    const title = queryByRole("heading", {
      level: 6,
      name: "Informations complémentaires",
    });
    expect(title).not.toBeInTheDocument();
  });

  test("Extra fields are shown along with dataset values", () => {
    const extraFields: ExtraField[] = [
      {
        id: "<id_1>",
        name: "referentiel",
        title: "Référentiel",
        hintText: "Choisissez un référentiel",
        type: "TEXT",
        data: {},
      },
      {
        id: "<id_2>",
        name: "sous_domaine",
        title: "Sous-domaine",
        hintText: "Choisissez un sous-domaine",
        type: "TEXT",
        data: {},
      },
    ];

    const extraFieldValues: ExtraFieldValue[] = [
      { extraFieldId: "<id_1>", value: "Référentiel A" },
    ];

    const { getByRole, getByText } = render(index, {
      data: {
        catalog: { ...catalog, extraFields },
        dataset: { ...dataset, extraFieldValues },
      },
    });

    const title = getByRole("heading", {
      level: 6,
      name: "Informations complémentaires",
    });
    expect(title).toBeInTheDocument();

    const referentielLabel = getByText("Référentiel");
    expect(referentielLabel).toBeInTheDocument();
    const referentielValue = referentielLabel.nextElementSibling;
    expect(referentielValue).toHaveTextContent("Référentiel A");

    const sousDomaineLabel = getByText("Sous-domaine");
    expect(sousDomaineLabel).toBeInTheDocument();
    const sousDomaineValue = sousDomaineLabel.nextElementSibling;
    expect(sousDomaineValue).toHaveTextContent("-");
  });
});
