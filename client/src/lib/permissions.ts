import type { Account } from "src/definitions/auth";
import type { Dataset } from "src/definitions/datasets";

export const canEditDataset = (dataset: Dataset, account: Account): boolean => {
  return dataset.catalogRecord.organization.siret === account.organizationSiret;
};
