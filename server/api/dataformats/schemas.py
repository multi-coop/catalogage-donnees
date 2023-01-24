from pydantic import BaseModel

from server.application.dataformats.validation import CreateDataFormatValidationMixin


class DataFormatCreate(CreateDataFormatValidationMixin, BaseModel):
    value: str
