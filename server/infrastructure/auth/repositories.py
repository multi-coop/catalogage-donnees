from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from server.domain.auth.entities import Account, PasswordUser
from server.domain.auth.exceptions import AccountDoesNotExist
from server.domain.auth.repositories import AccountRepository, PasswordUserRepository
from server.domain.common.types import ID

from ..database import Database
from .models import AccountModel, PasswordUserModel
from .transformers import (
    make_account_entity,
    make_account_instance,
    make_password_user_entity,
    make_password_user_instance,
    update_instance,
)


class SqlAccountRepository(AccountRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def _maybe_get_by(
        self, session: AsyncSession, *whereclauses: Any
    ) -> Optional[AccountModel]:
        stmt = select(AccountModel).where(*whereclauses)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Account]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(session, AccountModel.email == email)
            if instance is None:
                return None
            return make_account_entity(instance)

    async def get_by_api_token(self, api_token: str) -> Optional[Account]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(
                session, AccountModel.api_token == api_token
            )
            if instance is None:
                return None
            return make_account_entity(instance)


class SqlPasswordUserRepository(PasswordUserRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def _maybe_get_by(
        self, session: AsyncSession, *whereclauses: Any
    ) -> Optional[PasswordUserModel]:
        stmt = (
            select(PasswordUserModel)
            .join(AccountModel)
            .options(contains_eager(PasswordUserModel.account))
            .where(*whereclauses)
        )
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_by_email(self, email: str) -> Optional[PasswordUser]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(session, AccountModel.email == email)

            if instance is None:
                return None

            return make_password_user_entity(instance)

    async def insert(self, entity: PasswordUser) -> ID:
        async with self._db.session() as session:
            account_instance = make_account_instance(entity.account)
            session.add(account_instance)

            instance = make_password_user_instance(entity)
            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.account_id)

    async def update(self, entity: PasswordUser) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(
                session, PasswordUserModel.account_id == entity.account_id
            )

            if instance is None:
                raise AccountDoesNotExist(entity.account_id)

            update_instance(instance, entity)

            await session.commit()

    async def delete(self, account_id: ID) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by(
                session, PasswordUserModel.account_id == account_id
            )

            if instance is None:
                return

            await session.delete(instance)
            await session.commit()
