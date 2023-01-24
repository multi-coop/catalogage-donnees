from typing import List, Optional

from sqlalchemy import select

from server.domain.dataformats.entities import DataFormat
from server.domain.dataformats.repositories import DataFormatRepository

from ..database import Database
from .models import DataFormatModel
from .transformers import make_entity, make_instance


class SqlDataFormatRepository(DataFormatRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def insert(self, entity: DataFormat) -> Optional[int]:
        async with self._db.session() as session:
            async with session.begin():

                instance = make_instance(entity)

                session.add(instance)

            await session.refresh(instance)

            return instance.id

    async def get_all(self, ids: List[Optional[int]] = None) -> List[DataFormat]:
        async with self._db.session() as session:
            stmt = select(DataFormatModel)
            if ids is not None:
                stmt = stmt.where(DataFormatModel.id.in_(ids))
            result = await session.execute(stmt)
            items = result.unique().scalars()
            return [make_entity(item) for item in items]

    async def get_by_name(self, name: str) -> Optional[DataFormat]:
        async with self._db.session() as session:
            stmt = select(DataFormatModel).where(DataFormatModel.name == name)
            result = await session.execute(stmt)
            instance = result.unique().scalar_one_or_none()
            if instance is None:
                return None
            return make_entity(instance)

    async def get_by_id(self, id: int) -> Optional[DataFormat]:
        async with self._db.session() as session:
            stmt = select(DataFormatModel).where(DataFormatModel.id == id)
            result = await session.execute(stmt)
            instance = result.unique().scalar_one_or_none()
            if instance is None:
                return None
            return make_entity(instance)
