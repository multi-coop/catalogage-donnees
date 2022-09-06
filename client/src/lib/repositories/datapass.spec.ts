import { getDatapassUserInfoFromURLSearchParams } from "./datapass";

describe("datapass repository", () => {
  describe("getDatapassUserInfoFromURLSearchParams", () => {
    it("should return the required values from the search params", () => {
      const info = {
        email: "john@doe.com",
        organizations: [
          {
            name: "Ministry of Sound",
            siret: "11111111111",
          },
        ],
      };

      const token = "fake-token";

      const searchParams = new URLSearchParams({
        info: JSON.stringify(info),
        token,
      });

      const expectedResult = {
        token,
        info,
      };

      expect(getDatapassUserInfoFromURLSearchParams(searchParams)).toEqual(
        expectedResult
      );
    });

    it("should throw an error if a required info is missing -- no token has been provided", () => {
      const info = {
        email: "john@doe.com",
        organizations: [
          {
            name: "Ministry of Sound",
            siret: "11111111111",
          },
        ],
      };

      const searchParams = new URLSearchParams({
        info: JSON.stringify(info),
        // the token  is missing
      });

      expect(() =>
        getDatapassUserInfoFromURLSearchParams(searchParams)
      ).toThrow(Error);
    });

    it("should throw an error if a required info is missing -- no info provided", () => {
      const searchParams = new URLSearchParams({
        token: "fake-token",
      });

      expect(() =>
        getDatapassUserInfoFromURLSearchParams(searchParams)
      ).toThrow(Error);
    });
  });
});
