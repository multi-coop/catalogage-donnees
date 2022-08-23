import type { Maybe } from "$lib/util/maybe";

export interface LoginFormData {
  email: string;
  password: string;
}

export interface LoginApiRequestData {
  email: string;
  password: string;
}

export type UserRole = "USER" | "ADMIN";

export interface LoginApiResponseData {
  email: string;
  role: UserRole;
  apiToken: string;
}

export interface User {
  email: string;
  role: UserRole;
  apiToken: string;
}

export interface UserInfo {
  loggedIn: boolean;
  user: Maybe<User>;
}
