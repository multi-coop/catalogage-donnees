import { getFakeAccount } from "src/tests/factories/accounts";
import { getFakeCatalogRecord } from "src/tests/factories/catalog_records";
import { getFakeDataset } from "src/tests/factories/dataset";
import { getFakeOrganization } from "src/tests/factories/organizations";
import { canEditDataset } from "./permissions";

describe("permissions", () => {
  describe("canEditDataset", () => {
    test("Account with same SIRET as dataset can edit", () => {
      const organization = getFakeOrganization();
      const dataset = getFakeDataset({
        catalogRecord: getFakeCatalogRecord({ organization }),
      });
      const account = getFakeAccount({ organizationSiret: organization.siret });
      expect(canEditDataset(dataset, account)).toBeTruthy();
    });

    test("Account with different SIRET than dataset cannot edit", () => {
      const dataset = getFakeDataset();
      const account = getFakeAccount();
      expect(canEditDataset(dataset, account)).toBeFalsy();
    });
  });
});
