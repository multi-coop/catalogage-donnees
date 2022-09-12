import type { Organization } from "src/definitions/organization";

export const TEST_EMAIL = "catalogue.demo@yopmail.com";
export const TEST_PASSWORD = "password1234";
export const ADMIN_EMAIL = "admin@catalogue.data.gouv.fr";

export const TEST_ORGANIZATION: Organization = {
  siret: "44229377500031",
  name: "Ministère de la culture",
};
export const STATE_AUTHENTICATED = "./src/tests/e2e/storage/authenticated.json";
export const STATE_AUTHENTICATED_ADMIN =
  "./src/tests/e2e/storage/authenticated-admin.json";
