import { buildMailToString } from "./mail";

describe("buildMailToString", () => {
  it("should return a mailto string with subject", () => {
    const adresses = ["benjamin.frankin@mit.org", "tata@foo.org"];
    const body = `Salut${escape("\r\n")}Comment ça va?`;
    const expectedResult = `mailto:benjamin.frankin@mit.org,tata@foo.org?subject=tata&body=${body}`;
    const result = buildMailToString(adresses, "tata", body);
    expect(result).toStrictEqual(expectedResult);
  });
});
