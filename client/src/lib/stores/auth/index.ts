import type { UserInfo, Account } from "src/definitions/auth";
import { derived } from "svelte/store";
import { storable } from "../localStorage";

const validateExistingUserInfo = (value: UserInfo): boolean => {
  const { loggedIn, authenticatedUser } = value;
  return (loggedIn && !!authenticatedUser) || (!loggedIn && !authenticatedUser);
};

const userInfo = storable<UserInfo>(
  "user-info",
  { loggedIn: false, authenticatedUser: null },
  validateExistingUserInfo
);

export const account = derived(
  userInfo,
  (values) => values.authenticatedUser?.account
);

export const apiToken = derived(userInfo, (values) => {
  return values.authenticatedUser?.apiToken as string;
});

export const isAdmin = derived(account, (account) => {
  return account?.role === "ADMIN";
});

export const login = (account: Account, apiToken: string): void => {
  userInfo.set({ loggedIn: true, authenticatedUser: { account, apiToken } });
};

export const logout = (): void => {
  userInfo.set({ loggedIn: false, authenticatedUser: null });
};
