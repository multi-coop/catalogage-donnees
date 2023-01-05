from pydantic import BaseModel


class DataFormatView(BaseModel):
    id: int
    name: str
