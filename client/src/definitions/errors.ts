export class SearchParamsValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "SearchParamsValidationError";
  }
}
