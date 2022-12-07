from typing import Any, Generic, List, TypeVar, cast

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing_extensions import Annotated

from server.infrastructure.helpers.pydantic import Computed

T = TypeVar("T")


class Page(BaseModel):
    number: Annotated[int, Field(ge=1, le=10_000)] = 1
    size: Annotated[int, Field(ge=1)] = 10

    class Config:
        allow_mutation = False


class Pagination(GenericModel, Generic[T]):
    items: List[T]
    total_items: int
    page_size: int
    total_pages: Computed[int] = cast(
        Any, Field(Computed.Expr("math.ceil(total_items / page_size)"))
    )

    class Config:
        allow_mutation = False
