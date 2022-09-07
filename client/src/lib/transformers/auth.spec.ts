import { toAccount } from "./auth";

describe("transformers -- auth", () => {
  test("toAccount", () => {
    const data = {
      organization_siret: "<siret>",
      email: "<email>",
      role: "USER",
    };
    const result = toAccount(data);
    expect(result).toEqual({
      organizationSiret: "<siret>",
      email: "<email>",
      role: "USER",
    });
  });
});
