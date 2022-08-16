from typing import Any

import pytest
from pydantic import BaseModel

from server.domain.organizations.types import Siret


class TestSiret:
    @pytest.mark.parametrize(
        "value, expected_str",
        [
            pytest.param("65701934700404", "65701934700404", id="identity"),
            pytest.param("657 019 347 00404", "65701934700404", id="ignore-spaces"),
            pytest.param(Siret("65701934700404"), "65701934700404", id="instance"),
        ],
    )
    def test_valid(self, value: Any, expected_str: str) -> None:
        assert str(Siret(value)) == expected_str

    @pytest.mark.parametrize(
        "value, exc_type",
        [
            pytest.param(65701934700404, TypeError, id="non-string"),
            pytest.param("6570193470040a", ValueError, id="non-digits"),
            pytest.param("6570193470040", ValueError, id="less-than-14-digits"),
            pytest.param("657019347004044", ValueError, id="more-than-14-digits"),
        ],
    )
    def test_invalid(self, value: Any, exc_type: type) -> None:
        with pytest.raises(exc_type):
            Siret(value)

    def test_use_in_model(self) -> None:
        class Model(BaseModel):
            siret: Siret

        m = Model(siret="65701934700404")  # type: ignore
        assert m.siret == "65701934700404"

        with pytest.raises(ValueError):
            Model(siret="invalid")  # type: ignore

    def test_equals(self) -> None:
        assert Siret("65701934700404") == Siret("65701934700404")
        assert Siret("65701934700404") == "65701934700404"
        assert Siret("65701934700404") != 65701934700404
        assert Siret("65701934700404") != "test"
