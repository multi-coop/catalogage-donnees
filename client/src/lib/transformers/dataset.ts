import format from "date-fns/format";
import type { Dataset } from "src/definitions/datasets";

export const toPayload = (data: Partial<Record<keyof Dataset, any>>) => {
  const {
    entrypointEmail,
    contactEmails,
    updateFrequency,
    lastUpdatedAt,
    ...rest
  } = data;
  return {
    ...rest,
    entrypoint_email: entrypointEmail,
    contact_emails: contactEmails,
    first_published_at: new Date().toISOString(),
    update_frequency: updateFrequency,
    last_updated_at: new Date(lastUpdatedAt).toISOString(),
  };
};

export const toDataset = (item: any): Dataset => {
  const {
    created_at,
    entrypoint_email,
    contact_emails,
    update_frequency,
    last_updated_at,
    ...rest
  } = item;
  return {
    ...rest,
    createdAt: new Date(created_at),
    entrypointEmail: entrypoint_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    lastUpdatedAt: format(new Date(last_updated_at), "yyyy-MM-dd"),
  };
};
