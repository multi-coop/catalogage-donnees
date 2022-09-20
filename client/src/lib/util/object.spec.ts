import { omit } from "./object";

describe("miscalleneous", () => {
  describe("omit", () => {
    test("should omit props from an object", () => {
      const object = {
        foo: "hello",
        bar: "tata",
      };
      const result = omit(object, ["bar"]);

      expect(Object.keys(result).findIndex((item) => item === "bar")).toBe(-1);
    });
  });
});
