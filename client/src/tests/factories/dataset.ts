import type { Dataset } from "src/definitions/datasets";
import { buildFakeTag } from "./tags";

export const getFakeDataset = (dataset: Partial<Dataset> = {}): Dataset => {
  return {
    id: dataset.id || "xxx-xxx-xxx",
    catalogRecord: dataset.catalogRecord || {
      createdAt: new Date(),
      organization: {
        name: "Fake",
        siret: "00000000000000",
        logoUrl:
          "https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/culture/logo.svg",
      },
    },
    title: dataset.title || "Mon jeu de donnée",
    description: dataset.description || "un joli jeu de donnée",
    formats: dataset.formats || [],
    producerEmail: dataset.producerEmail || "jane.doe@beta.gouv.fr",
    contactEmails: dataset.contactEmails || ["contact@beta.gouv.fr"],
    service: dataset.service || "La Drac",
    technicalSource: dataset.technicalSource || null,
    updateFrequency: dataset.updateFrequency || "daily",
    lastUpdatedAt: dataset.lastUpdatedAt || new Date(),
    geographicalCoverage: dataset.geographicalCoverage || "europe",
    url: dataset.url || null,
    license: dataset.license || null,
    tags: dataset.tags || [buildFakeTag()],
    extraFieldValues: [],
    publicationRestriction: "no_restriction",
  };
};
