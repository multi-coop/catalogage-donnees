from pydantic import BaseModel, validator


class GetCatalogExtraFields(BaseModel):
    @validator("organization_id", check_fields=False)
    def check_value_at_least_one(cls, organization_id: str) -> str:
        if not organization_id:
            raise ValueError("must have a organization_id")
        return organization_id
