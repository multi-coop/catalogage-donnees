import type { Account } from "src/definitions/auth";

export const toAccount = (data: any): Account => {
  return {
    organizationSiret: data.organization_siret,
    email: data.email,
    role: data.role,
  };
};
