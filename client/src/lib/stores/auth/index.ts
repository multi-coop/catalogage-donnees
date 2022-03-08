import type { UserInfo, User } from "src/definitions/auth";
import { derived } from "svelte/store";
import { storable } from "../localStorage";

const validateExistingUserInfo = (value: UserInfo): boolean => {
  const { loggedIn, user } = value;
  return (loggedIn && !!user) || (!loggedIn && !user);
};

const userInfo = storable<UserInfo>(
  "user-info",
  { loggedIn: false, user: null },
  validateExistingUserInfo
);

export const isLoggedIn = derived(userInfo, (values) => values.loggedIn);

export const user = derived(userInfo, (values) => values.user);

export const login = (user: User) => {
  userInfo.set({ loggedIn: true, user });
};

export const logout = () => {
  userInfo.set({ loggedIn: false, user: null });
};