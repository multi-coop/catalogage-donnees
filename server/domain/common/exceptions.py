from typing import Any


class DoesNotExist(Exception):
    entity_name: str

    def __init__(self, pk: Any) -> None:
        super().__init__(f"{self.entity_name} not found: {pk!r}")


class AlreadyExists(Exception):
    entity_name: str

    def __init__(self, pk: Any) -> None:
        super().__init__(f"{self.entity_name} already exists: {pk!r}")
