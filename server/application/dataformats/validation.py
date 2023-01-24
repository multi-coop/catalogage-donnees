from pydantic import BaseModel, validator


class CreateDataFormatValidationMixin(BaseModel):
    @validator("value", check_fields=False)
    def check_value_at_least_one(cls, value: str) -> str:
        if not value:
            raise ValueError("dataformat must have a value")
        return value
