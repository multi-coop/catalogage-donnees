from typing import List, Optional

from pydantic import BaseModel, validator


class CreateDatasetValidationMixin(BaseModel):
    @validator("format_ids", check_fields=False)
    def check_formats_at_least_one(cls, value: List[int]) -> List[int]:
        if not value or len(value) == 0:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails", check_fields=False)
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value


class UpdateDatasetValidationMixin(BaseModel):
    @validator("title", check_fields=False)
    def check_title_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("title must not be empty")
        return value

    @validator("description", check_fields=False)
    def check_description_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("description must not be empty")
        return value

    @validator("service", check_fields=False)
    def check_service_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("service must not be empty")
        return value

    @validator("format_ids", check_fields=False)
    def check_formats_at_least_one(cls, value: List[int]) -> List[int]:
        if not value or len(value) == 0:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails", check_fields=False)
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value

    @validator("url", check_fields=False)
    def check_url_not_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value:
            raise ValueError("url must not be empty")
        return value
