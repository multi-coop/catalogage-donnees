import type { Maybe } from "$lib/util/maybe";

export interface LoginFormData {
  email: string;
  password: string;
}

export interface PasswordLoginData {
  email: string;
  password: string;
}

export type UserRole = "USER" | "ADMIN";

export interface Account {
  organizationSiret: string;
  email: string;
  role: UserRole;
}

export interface AuthenticatedUser {
  account: Account;
  apiToken: string;
}

export interface UserInfo {
  loggedIn: boolean;
  authenticatedUser: Maybe<AuthenticatedUser>;
}
