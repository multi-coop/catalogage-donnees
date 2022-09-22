import { range } from "./array";

describe("range", () => {
  const startEndCases: [number, number, number[]][] = [
    [1, 1, []],
    [2, 1, []],
    [2, 2, []],
    [1, 2, [1]],
    [1, 3, [1, 2]],
    [2, 5, [2, 3, 4]],
    [-3, 2, [-3, -2, -1, 0, 1]],
  ];

  test.each(startEndCases)(
    "when start=%s and end=%s",
    (start, end, expected) => {
      expect(range(start, end)).toStrictEqual(expected);
    }
  );

  const endCases: [number, number[]][] = [
    [0, []],
    [1, [0]],
    [4, [0, 1, 2, 3]],
    [-3, []],
  ];

  test.each(endCases)("when end=%s", (end, expected) => {
    expect(range(end)).toStrictEqual(expected);
  });
});
