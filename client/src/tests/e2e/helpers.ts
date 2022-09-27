export const getToolsPassword = (email: string): string => {
  const passwords = JSON.parse(process.env.TOOLS_PASSWORDS || "{}");
  const password = passwords[email];
  if (!password) {
    throw new Error(`Password for ${email} not defined in TOOLS_PASSWORDS`);
  }
  return password;
};
