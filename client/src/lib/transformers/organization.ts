import type { Organization } from "src/definitions/organization";

type RawOrganization = Omit<Organization, "logoUrl"> & { logo_url: string };

export const toOrganization = (
  rawOrganization: RawOrganization
): Organization => {
  return {
    ...rawOrganization,
    logoUrl: rawOrganization.logo_url,
  };
};
