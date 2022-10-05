import type { Account } from "src/definitions/auth";
import type { Dataset } from "src/definitions/datasets";
import { Maybe } from "./util/maybe";

export const canEditDataset = (
  dataset: Dataset,
  account: Maybe<Account>
): boolean => {
  return (
    Maybe.Some(account) &&
    dataset.catalogRecord.organization.siret === account.organizationSiret
  );
};
