export const omit = <T extends Record<string, unknown>, K extends keyof T>(
  obj: T,
  props: K[]
): Omit<T, K> => {
  const temp = { ...obj };
  props.forEach((prop) => delete temp[prop]);
  return temp;
};
