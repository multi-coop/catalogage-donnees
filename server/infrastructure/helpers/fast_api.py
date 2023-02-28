from typing import Any

import pydantic
from fastapi import Depends, HTTPException, Query
from pydantic import Json, ValidationError


def json_param(param_name: str, model: Any, **query_kwargs):
    """Parse JSON-encoded query parameters as pydantic models.
    The function returns a `Depends()` instance that takes the JSON-encoded value from
    the query parameter `param_name` and converts it to a Pydantic model, defined
    by the `model` attribute.
    """

    def get_parsed_object(value: Json = Query(alias=param_name, **query_kwargs)):
        try:
            return pydantic.parse_obj_as(model, value)
        except ValidationError as err:
            raise HTTPException(400, detail=err.errors())

    return Depends(get_parsed_object)
