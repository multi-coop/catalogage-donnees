import { writable, type Readable } from "svelte/store";

/**
 * @returns A new store that sends a value once `store` has not been called for `delay` milliseconds.
 *
 * Inspired by: https://docs-lodash.com/v4/debounce/
 */
export const debounce = <T>(store: Readable<T>, delay: number): Readable<T> => {
  const newStore = writable<T>();

  let timer: NodeJS.Timeout;

  store.subscribe((value) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      newStore.set(value);
    }, delay);
  });

  return newStore;
};
