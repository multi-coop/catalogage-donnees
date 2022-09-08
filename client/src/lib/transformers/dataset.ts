import type {
  Dataset,
  DatasetCreateData,
  DatasetUpdateData,
} from "src/definitions/datasets";
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
  data: DatasetCreateData | DatasetUpdateData
): { [K: string]: unknown } => {
  const extra_field_values = (data.extraFieldValues || []).map(
    ({ extraFieldId, value }) => ({
      extra_field_id: extraFieldId,
      value,
    })
  );

  return {
    ...transformKeysToUnderscoreCase(omit(data, ["extraFieldValues"])),
    extra_field_values,
  };
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
    extra_field_values,
    ...rest
  } = item;
  const { created_at, organization } = catalog_record;
  return {
    ...rest,
    catalogRecord: {
      createdAt: new Date(created_at),
      organization,
    },
    producerEmail: producer_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    lastUpdatedAt: last_updated_at ? new Date(last_updated_at) : null,
    url,
    extraFieldValues: extra_field_values.map(({ extra_field_id, value }) => ({
      extraFieldId: extra_field_id,
      value,
    })),
  };
};
