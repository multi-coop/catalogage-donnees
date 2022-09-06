import type { Account } from "src/definitions/auth";

export const toAccount = (data: any): Account => {
  return {
    email: data.email,
    role: data.role,
  };
};
