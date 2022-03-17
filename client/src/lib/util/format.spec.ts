import * as datefns from "date-fns";
import { pluralize, capitalize, formatDaysMonthsOrYearsToNow } from "./format";

test("pluralize", () => {
  expect(`0 résultat${pluralize(0, "", "s")}`).toBe("0 résultats");
  expect(`1 ${pluralize(1, "cheval", "chevaux")}`).toBe("1 cheval");
  expect(`2 jour${pluralize(2, "", "s")}`).toBe("2 jours");
  expect(`3 ${pluralize(3, "cheval", "chevaux")}`).toBe("3 chevaux");
});

test.each([
  ["", ""],
  ["Test", "Test"],
  ["test", "Test"],
  ["test it", "Test it"],
])("capitalize", (value, expected) => {
  expect(capitalize(value)).toBe(expected);
});

describe("formatDaysMonthsOrYearsToNow", () => {
  test.each([
    [new Date(), "aujourd'hui"],
    [datefns.subSeconds(datefns.startOfDay(new Date()), 1), "hier"],
    [datefns.subDays(new Date(), 1), "hier"],
    [datefns.subDays(new Date(), 2), "il y a 2 jours"],
    [datefns.subDays(new Date(), 27), "il y a 27 jours"],
    [datefns.subDays(new Date(), 31), "il y a 1 mois"],
    [datefns.subMonths(new Date(), 1), "il y a 1 mois"],
    [datefns.subMonths(new Date(), 2), "il y a 2 mois"],
    [datefns.subMonths(new Date(), 11), "il y a 11 mois"],
    [datefns.subMonths(new Date(), 12), "il y a 1 an"],
    [datefns.subYears(new Date(), 2), "il y a 2 ans"],
    [datefns.subYears(new Date(), 10), "il y a 10 ans"],
  ])("formats successfully", (date, expected) => {
    const actual = formatDaysMonthsOrYearsToNow(date);
    expect(actual).toBe(expected);
    expect(actual.length).toBeLessThanOrEqual(15); // Short enough to fit on a single line when displayed.
  });

  test("errors", () => {
    expect(() =>
      formatDaysMonthsOrYearsToNow(datefns.addDays(new Date(), 1))
    ).toThrowError(/date should be in the past/);
  });
});