export const escape = (value: string): string => {
  // See: https://stackoverflow.com/a/3561711
  return value.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
};

export const camelToSnake = (str: string): string => {
  return str.replace(/[A-Z]/g, (c) => {
    return "_" + c.toLowerCase();
  });
};
