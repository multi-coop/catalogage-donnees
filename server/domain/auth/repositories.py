from typing import Optional

from server.seedwork.domain.repositories import Repository

from ..common.types import ID, id_factory
from .entities import Account, DataPassUser, PasswordUser


class AccountRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_by_email(self, email: str) -> Optional[Account]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_api_token(self, api_token: str) -> Optional[Account]:
        raise NotImplementedError  # pragma: no cover


class PasswordUserRepository(Repository):
    async def get_by_email(self, email: str) -> Optional[PasswordUser]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: PasswordUser) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def update(self, entity: PasswordUser) -> None:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, id: ID) -> None:
        raise NotImplementedError  # pragma: no cover


class DataPassUserRepository(Repository):
    async def get_by_email(self, email: str) -> Optional[DataPassUser]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: DataPassUser) -> ID:
        raise NotImplementedError  # pragma: no cover
