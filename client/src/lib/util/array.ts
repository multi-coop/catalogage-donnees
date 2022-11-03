/**
 * @returns An array of integers from `start` (included) to `end` (excluded).
 */
export const range = (start: number, end?: number): number[] => {
  if (end === undefined) {
    end = start;
    start = 0;
  }
  const length = end - start;
  return Array.from({ length }, (_, idx) => start + idx);
};

interface ArrayWithItems<T> extends Array<T> {
  0: T; // Ensure array has at least one item.
}

export const hasItems = <T>(arr: T[]): arr is ArrayWithItems<T> => {
  return arr.length > 0;
};

export const first = <T>(arr: ArrayWithItems<T>): T => {
  return arr[0];
};

export const last = <T>(arr: ArrayWithItems<T>): T => {
  return arr[arr.length - 1];
};

export const removeEmptyValues = (items: Array<string | null>): Array<string> =>
  items.filter((item) => item) as string[];
