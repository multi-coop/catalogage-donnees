import uuid
from typing import NewType

from pydantic import BaseModel

ID = NewType("ID", uuid.UUID)


def id_factory() -> ID:
    return ID(uuid.uuid4())


class Skip(BaseModel):
    """
    A marker class for when an operation should be skipped.
    """
