import type { QueryParamRecord } from "src/definitions/url";
import { Maybe } from "./maybe";

/**
 * Create an URL query string, including a leading "?", dropping any null or undefined values.
 */
export const toQueryString = (items: QueryParamRecord): string => {
  return patchQueryString(new URLSearchParams(), items);
};

export const patchQueryString = (
  params: URLSearchParams,
  items: QueryParamRecord
): string => {
  const newParams = new URLSearchParams(params);
  items.forEach(([name, value]) => {
    if (Maybe.Some(value)) {
      newParams.set(name, value.toString());
    } else {
      newParams.delete(name);
    }
  });
  const qs = newParams.toString();
  return `?${qs}`;
};
