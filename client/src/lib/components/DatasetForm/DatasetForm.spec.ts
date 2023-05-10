/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import { render, fireEvent } from "@testing-library/svelte";
import type {
  DatasetFormData,
  DatasetFormInitial,
} from "src/definitions/datasets";
import { login, logout } from "$lib/stores/auth";
import { buildFakeTag } from "src/tests/factories/tags";
import type { Catalog } from "src/definitions/catalogs";
import type { Organization } from "src/definitions/organization";
import type { ExtraField } from "src/definitions/extraField";

describe("Test the dataset form", () => {
  beforeAll(() =>
    login(
      {
        organizationSiret: "<siret>",
        email: "john@domain.org",
        role: "USER",
      },
      "abcd1234"
    )
  );

  afterAll(() => logout());

  const organization: Organization = {
    siret: "<siret>",
    name: "Org 1",
    logoUrl:
      "https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/culture/logo.svg",
  };

  const catalog: Catalog = { organization, extraFields: [] };

  const extraField: ExtraField = {
    id: "<extraField1Id>",
    name: "referentiel",
    title: "Référentiel",
    hintText: "Remplissez cette information SVP",
    type: "TEXT",
    data: {},
  };

  const catalogWithExtraFields: Catalog = {
    organization,
    extraFields: [extraField],
  };

  test('The "title" field is present', () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const title = getByLabelText("Nom du jeu de données", { exact: false });
    expect(title).toBeInTheDocument();
    expect(title).toBeRequired();
  });

  test('The "description" field is present', () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const description = getByLabelText("Description", { exact: false });
    expect(description).toBeInTheDocument();
    expect(description).toBeRequired();
  });

  test('The "formats" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, {
      catalog,
      formats: [
        {
          id: 55,
          name: "fichier tabulaire",
        },
      ],
    });
    const formatfield = getByLabelText("Format(s) des données", {
      exact: false,
    });
    expect(formatfield).toBeInTheDocument();
  });

  test('The "geographicalCoverage" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const geographicalCoverage = getByLabelText("Couverture géographique", {
      exact: false,
    });
    expect(geographicalCoverage).toBeInTheDocument();
    expect(geographicalCoverage).toBeRequired();
  });

  test('The "technicalSource" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const technicalSource = getByLabelText("Système d'information source", {
      exact: false,
    });
    expect(technicalSource).toBeInTheDocument();
    expect(technicalSource).not.toBeRequired();
  });

  test('The "tags" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const tags = getByLabelText("Mots-clés", {
      exact: false,
    });
    expect(tags).toBeInTheDocument();
  });

  test('The "producerEmail" field is present', () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const producerEmail = getByLabelText(
      "Adresse e-mail du service producteur",
      {
        exact: false,
      }
    );
    expect(producerEmail).toBeInTheDocument();
    expect(producerEmail).not.toBeRequired();
    expect(producerEmail).toHaveAttribute("type", "email");
  });

  test('The "contact emails" field is present', () => {
    const { getAllByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const inputs = getAllByLabelText(/Contact \d/) as HTMLInputElement[];
    expect(inputs.length).toBe(1);
    expect(inputs[0]).toHaveAttribute("type", "email");
    expect(inputs[0]).not.toBeRequired();
    expect(inputs[0].value).toBe("john@domain.org");
  });

  test('The "contact emails" field requires at least one value', async () => {
    const { getAllByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const inputs = getAllByLabelText(/Contact \d/) as HTMLInputElement[];
    expect(inputs.length).toBe(1);
    await fireEvent.input(inputs[0], { target: { value: "" } });
    expect(inputs[0]).toBeRequired();
  });

  test('The "url" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const url = getByLabelText("Lien vers les données", {
      exact: false,
    });
    expect(url).toBeInTheDocument();
    expect(url).not.toBeRequired();
  });

  test('The "license" field is present', async () => {
    const { getByLabelText } = render(DatasetForm, { catalog, formats: [] });
    const license = getByLabelText("Licence de réutilisation", {
      exact: false,
    });
    expect(license).toBeInTheDocument();
    expect(license).not.toBeRequired();
  });

  test("Extra fields are present", () => {
    const { getByLabelText } = render(DatasetForm, {
      catalog: catalogWithExtraFields,
      formats: [],
    });
    const extraReferentiel = getByLabelText("Référentiel", { exact: false });
    expect(extraReferentiel).toBeInTheDocument();
    expect(extraReferentiel).not.toBeRequired();
  });

  test("The submit button is present", () => {
    const { getByRole } = render(DatasetForm, { catalog, formats: [] });
    expect(getByRole("button", { name: /Publier/i })).toBeInTheDocument();
  });

  test("The submit button displays a loading text when loading", async () => {
    const props = {
      catalog,
      submitLabel: "Envoyer",
      loadingLabel: "Ça charge...",
      formats: [
        {
          id: 33,
          name: "Fichier Tabulaire",
        },
      ],
    };

    const { getByRole, rerender } = render(DatasetForm, { props });
    expect(getByRole("button", { name: "Envoyer" })).toBeInTheDocument();

    rerender({ props: { ...props, loading: true } });
    expect(getByRole("button", { name: /Ça charge/i })).toBeInTheDocument();
  });

  test("The fields are initialized with initial values", async () => {
    const fakeTag = buildFakeTag({ name: "Architecture" });
    const initial: DatasetFormInitial = {
      catalogRecord: {
        createdAt: new Date(),
        organization: {
          name: "Fake",
          siret: "<siret>",
          logoUrl:
            "https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/culture/logo.svg",
        },
      },
      title: "Titre initial",
      description: "Description initiale",
      formats: [
        {
          id: 33,
          name: "Fichier Tabulaire",
        },
      ],
      producerEmail: "service.initial@mydomain.org",
      contactEmails: ["person@mydomain.org"],
      service: "A nice service",
      lastUpdatedAt: new Date("2022-02-01"),
      updateFrequency: "never",
      geographicalCoverage: "europe",
      technicalSource: "foo/bar",
      url: "https://data.gouv.fr/datasets/example",
      license: "Licence Ouverte",
      tags: [fakeTag],
      extraFieldValues: [{ extraFieldId: "<extraField1Id>", value: "Réponse" }],
      publicationRestriction: "draft",
    };
    const props = {
      catalog: catalogWithExtraFields,
      initial,
      formats: [
        {
          id: 33,
          name: "Fichier Tabulaire",
        },
      ],
    };

    const { getByLabelText, getAllByLabelText, container, getAllByText } =
      render(DatasetForm, { props });

    const title = getByLabelText("Nom du jeu de données", {
      exact: false,
    }) as HTMLInputElement;
    expect(title.value).toBe("Titre initial");

    const description = getByLabelText("Description", {
      exact: false,
    }) as HTMLInputElement;
    expect(description.value).toBe("Description initiale");

    container.querySelector(`input[value="Fichier Tabulaire"]`);

    const producerEmail = getByLabelText(
      "Adresse e-mail du service producteur",
      {
        exact: false,
      }
    ) as HTMLInputElement;
    expect(producerEmail.value).toBe("service.initial@mydomain.org");

    const contactEmails = getAllByLabelText(/Contact \d/);
    expect(contactEmails.length).toBe(1);
    expect(contactEmails[0]).toHaveValue("person@mydomain.org");
    expect(contactEmails[0]).not.toBeRequired();

    const lastUpdatedAt = getByLabelText("Date de la dernière mise à jour", {
      exact: false,
    }) as HTMLInputElement;
    expect(lastUpdatedAt.value).toBe("2022-02-01");

    const updateFrequency = getByLabelText("Fréquence de mise à jour", {
      exact: false,
    }) as HTMLSelectElement;
    expect(updateFrequency.value).toBe("never");

    const technicalSource = getByLabelText("Système d'information source", {
      exact: false,
    }) as HTMLSelectElement;
    expect(technicalSource.value).toBe("foo/bar");

    const url = getByLabelText("Lien vers les données", {
      exact: false,
    }) as HTMLSelectElement;
    expect(url.value).toBe("https://data.gouv.fr/datasets/example");

    const tags = getAllByText(fakeTag.name);
    expect(tags).toHaveLength(1);

    const license = getByLabelText("Licence de réutilisation", {
      exact: false,
    }) as HTMLInputElement;
    expect(license.value).toBe("Licence Ouverte");

    const extraReferentiel = getByLabelText("Référentiel", {
      exact: false,
    }) as HTMLInputElement;
    expect(extraReferentiel.value).toBe("Réponse");
  });

  test("Null or empty fields are correctly submitted as null", async () => {
    const initial: DatasetFormInitial = {
      catalogRecord: {
        createdAt: new Date(),
        organization: {
          name: "Fake",
          siret: "<siret>",
          logoUrl:
            "https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/culture/logo.svg",
        },
      },
      title: "Titre initial",
      description: "Description initiale",
      formats: [
        {
          name: "fichier Tabulaire",
          id: 55,
        },
      ],
      producerEmail: "",
      contactEmails: ["person@mydomain.org"],
      service: "A nice service",
      lastUpdatedAt: null,
      updateFrequency: null,
      geographicalCoverage: "europe",
      technicalSource: "foo/bar",
      url: "",
      license: null,
      tags: [buildFakeTag()],
      extraFieldValues: [{ extraFieldId: "<extraField1Id>", value: "" }],
      publicationRestriction: "draft",
    };
    const props = {
      catalog,
      initial,
      formats: [
        {
          name: "fichier Tabulaire",
          id: 55,
        },
      ],
    };
    const { getByLabelText, getByRole, component } = render(DatasetForm, {
      props,
    });

    const lastUpdatedAt = getByLabelText("Date de la dernière mise à jour", {
      exact: false,
    }) as HTMLInputElement;
    expect(lastUpdatedAt.value).toBe("");

    const updateFrequency = getByLabelText("Fréquence de mise à jour", {
      exact: false,
    }) as HTMLSelectElement;

    // Simulate touching the fields. This sends HTML values such as "" (empty date or select value)
    // which should be handled as null.
    await fireEvent.blur(lastUpdatedAt);
    await fireEvent.blur(updateFrequency);

    const form = getByRole("form");
    await fireEvent.submit(form);
    const submittedValue = await new Promise<DatasetFormData>((resolve) => {
      component.$on("save", (event) => resolve(event.detail));
    });
    expect(submittedValue.lastUpdatedAt).toBe(null);
    expect(submittedValue.updateFrequency).toBe(null);
    expect(submittedValue.producerEmail).toBe(null);
    expect(submittedValue.url).toBe(null);
    expect(submittedValue.license).toBe(null);
    expect(submittedValue.extraFieldValues).toEqual([]);
  });
});
