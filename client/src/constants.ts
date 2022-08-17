import type { DataFormat, UpdateFrequency } from "./definitions/datasets";


// Note : the / page (the home page) is "semi public". This page layout and information displayed depends whether the user is connected or not
export const PUBLIC_PAGES = ["/login", "/"];

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

export const UPDATE_FREQUENCY_LABELS: { [K in UpdateFrequency]: string } = {
  never: "Aucune (contribution ponctuelle)",
  realtime: "Permanente (temps réel)",
  daily: "Quotidienne (ou plusieurs fois par jour)",
  weekly: "Hebdomadaire (ou plusieurs fois par semaine)",
  monthly: "Mensuelle (ou plusieurs fois pas mois)",
  yearly: "Annuel (ou plusieurs fois par an)",
};

export const DATASETS_PER_PAGE = 50;
