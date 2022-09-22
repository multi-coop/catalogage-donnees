import type { Account } from "src/definitions/auth";
import type { Dataset } from "src/definitions/datasets";

export default {
  dataset: {
    edit: (dataset: Dataset, account: Account): boolean => {
      return (
        dataset.catalogRecord.organization.siret === account.organizationSiret
      );
    },
  },
};
