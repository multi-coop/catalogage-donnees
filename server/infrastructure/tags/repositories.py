from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.common.types import ID, id_factory
from server.domain.tags.entities import Tag
from server.domain.tags.repositories import TagRepository

from ..database import Database
from .models import TagModel
from .transformers import make_entity, make_instance


class SqlTagRepository(TagRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    def make_id(self) -> ID:
        return id_factory()

    async def get_all(self, *, ids: List[ID] = None) -> List[Tag]:
        async with self._db.session() as session:
            stmt = select(TagModel)
            if ids is not None:
                stmt = stmt.where(TagModel.id.in_(ids))
            stmt = stmt.order_by(TagModel.name)
            result = await session.execute(stmt)
            return [make_entity(instance) for instance in result.scalars().all()]

    async def _maybe_get_by_id(
        self, session: AsyncSession, id_: ID
    ) -> Optional[TagModel]:
        stmt = select(TagModel).where(TagModel.id == id_)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id_: ID) -> Optional[Tag]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id_)

            if instance is None:
                return None

            return make_entity(instance)

    async def delete_many_by_id(self, ids_: List[ID]) -> List[ID]:
        async with self._db.session() as session:
            stmt = delete(TagModel).where(TagModel.id.in_(ids_))
            await session.execute(stmt)

            return ids_

    async def insert(self, entity: Tag) -> ID:
        async with self._db.session() as session:
            async with session.begin():
                instance = make_instance(entity)
                session.add(instance)

            await session.refresh(instance)

            return ID(instance.id)
