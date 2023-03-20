import type { Organization } from "src/definitions/organization";

type RawOrganization = Omit<Organization, "logo_url"> & { logo_url: string };

export const toOrganization = (
  rawOrganization: RawOrganization
): Organization => {
  return {
    ...rawOrganization,
    logo_url: rawOrganization.logo_url,
  };
};
