import type { Dataset } from "src/definitions/datasets";
import { omit } from "../util/object.js";

export const camelToUnderscore = (key: string): string => {
  return key.replace(/([A-Z])/g, "_$1").toLowerCase();
};

export const transformKeysToUnderscoreCase = (object: {
  [K: string]: unknown;
}): { [K: string]: unknown } => {
  return Object.keys(object).reduce((previous, current) => {
    return {
      ...previous,
      [camelToUnderscore(current)]: object[current],
    };
  }, {});
};

export const toPayload = (
  data: Partial<Record<keyof Dataset, any>>
): { [K: string]: unknown } => {
  return transformKeysToUnderscoreCase(omit(data, ["catalogRecord"]));
};

export const toDataset = (item: any): Dataset => {
  const {
    catalog_record,
    producer_email,
    contact_emails,
    update_frequency,
    last_updated_at,
    geographical_coverage,
    technical_source,
    url,
    ...rest
  } = item;
  const { created_at } = catalog_record;
  return {
    ...rest,
    catalogRecord: {
      createdAt: new Date(created_at),
    },
    producerEmail: producer_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    lastUpdatedAt: last_updated_at ? new Date(last_updated_at) : null,
    url,
  };
};
