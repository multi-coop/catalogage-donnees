import type { Organization } from "src/definitions/organization";

type RawOrganization = Omit<Organization, "logoUrl"> & { logoUrl: string };

export const toOrganization = (
  rawOrganization: RawOrganization
): Organization => {
  return {
    ...rawOrganization,
    logoUrl: rawOrganization.logoUrl,
  };
};
