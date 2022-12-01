import type {
  DataFormat,
  PublicationRestriction,
  UpdateFrequency,
} from "./definitions/datasets";
import type { TrustedHtml } from "./lib/util/html";

export const SITE_TITLE = "catalogue.data.gouv.fr";

export const SITE_DESCRIPTION =
  "Un service pour aider les administrations à créer, gérer et ouvrir leurs catalogues.";

export const HOME_SECTION_NAME = "Accueil";

const STATIC_PAGES = [
  "/mentions-legales",
  "/vie-privee",
  "/login",
  "/declaration-daccessibilite",
  "/auth/datapass/create-organization",
  "/auth/datapass/login",
  "/auth/datapass/pick-organization",
];

export const NON_AUTH_GUARDED_PAGES = [...STATIC_PAGES, "/"];

export const DATA_FORMAT_LABELS: { [K in DataFormat]: string } = {
  file_tabular: "Fichier tabulaire (XLS, XLSX, CSV, ...)",
  file_gis: "Fichier SIG (Shapefile, ...)",
  api: "API (REST, GraphQL, ...)",
  database: "Base de données",
  website: "Site web",
  other: "Autre",
};

export const DATA_FORMAT_SHORT_NAMES: { [K in DataFormat]: string } = {
  file_tabular: "CSV",
  file_gis: "SIG",
  api: "API",
  database: "BDD",
  website: "Web",
  other: "Autre",
};

export const PUBLICATION_RESTRICTIONS_OPTIONS: {
  [K in PublicationRestriction]: string | TrustedHtml;
} = {
  no_restriction: "non",
  draft: "Oui, car cette fiche n’est pas achevée",
  legal_restriction: {
    content:
      "Oui, car les informations contribuées contiennent des &nbsp; <a href='https://guides.etalab.gouv.fr/juridique/ouverture/#que-faire-si-mes-documents-administratifs-contiennent-des-secrets-legaux' rel='noopener' target='_blank'> secrets légaux</a>",
    isHtml: true,
  },
};

export const PUBLICATION_RESTRICTION: {
  [K in PublicationRestriction]: string;
} = {
  no_restriction: "no_restriction",
  draft: "draft",
  legal_restriction: "legal_restriction",
};

export const UPDATE_FREQUENCY_LABELS: { [K in UpdateFrequency]: string } = {
  never: "Aucune (contribution ponctuelle)",
  realtime: "Permanente (temps réel)",
  daily: "Quotidienne (ou plusieurs fois par jour)",
  weekly: "Hebdomadaire (ou plusieurs fois par semaine)",
  monthly: "Mensuelle (ou plusieurs fois pas mois)",
  yearly: "Annuel (ou plusieurs fois par an)",
};

export const DATASETS_PER_PAGE = 50;

export const USER_DOCUMENTATION_LINK =
  "https://github.com/etalab/catalogage-donnees/wiki/Documentation-%C3%A0-destination-des-utilisateurs";
export const REGISTER_ORGANIZATION_LINK =
  "https://github.com/etalab/catalogage-donnees/wiki/Documentation-%C3%A0-destination-des-utilisateurs#comment-enregistrer-une-organisation-sur-cataloguedatagouvfr-";

export const CONTACT_EMAIL = "catalogue@data.gouv.fr";
