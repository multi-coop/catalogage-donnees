import { getFakeDataset } from "src/tests/factories/dataset";
import {
  toDataset,
  toPayload,
  camelToUnderscore,
  transformKeysToUnderscoreCase,
} from "./dataset";

describe("transformers -- dataset", () => {
  test("transformKeysToUnderscoreCase", () => {
    const text = "helloWorld";
    const result = camelToUnderscore(text);
    expect(result).toBe("hello_world");
  });

  test("transformKeysToUnderscoreCase", () => {
    const input = {
      helloWorld: "hello",
      fooBaz: "hello",
    };
    const result = transformKeysToUnderscoreCase(input);

    expect(Object.keys(result).every((key) => key.includes("_"))).toBe(true);
  });

  test("toPayload", () => {
    const data = {
      ...getFakeDataset(),
      organizationSiret: "<siret>",
      tagIds: [],
      formatIds: [],
    };
    const result = toPayload(data);
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      true
    );
  });

  test("toDataset", () => {
    const data = toPayload({
      ...getFakeDataset(),
      organizationSiret: "<siret>",
      tagIds: [],
      formatIds: [],
    });
    const result = toDataset({
      ...data,
      catalog_record: {
        created_at: new Date().toISOString(),
        organization: { name: "Fake", siret: "<siret>" },
      },
    });
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      false
    );
  });
});
