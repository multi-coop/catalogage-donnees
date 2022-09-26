from typing import Any, cast

import pytest
from pydantic import BaseModel, Field, ValidationError

from server.infrastructure.helpers.pydantic import Computed


def test_computed() -> None:
    class Square(BaseModel):
        side: float
        area: Computed[float] = cast(Any, Field(Computed.Expr("side ** 2")))

    square = Square(side=3)
    assert square.area == 9
    assert square.dict() == {"side": 3, "area": 9}

    square.side = 4
    assert square.area == 9  # Watching changes is not supported


def test_computed_validate() -> None:
    class Model(BaseModel):
        x: Computed[int] = cast(Any, Field(Computed.Expr("'not an int'")))

    with pytest.raises(ValidationError) as ctx:
        Model()

    (error,) = ctx.value.errors()
    assert error["loc"] == ("x",)
    assert error["type"] == "value_error"
