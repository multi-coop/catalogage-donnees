import type { Account } from "src/definitions/auth";
import { getFakeSiret } from "./organizations";

export const getFakeAccount = (obj: Partial<Account> = {}): Account => {
  return {
    organizationSiret: obj.organizationSiret || getFakeSiret(),
    email: obj.email || "test@mydomain.org",
    role: obj.role || "USER",
  };
};
