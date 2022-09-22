/**
 * @returns A random integer between `start` (included) and `end` (excluded)
 */
export const randint = (start: number, end: number): number => {
  return Math.floor(start + Math.random() * (end - start));
};
