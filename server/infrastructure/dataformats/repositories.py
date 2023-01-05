from typing import List
from server.domain.common.types import ID
from server.domain.dataformats.entities import DataFormat

from sqlalchemy import select
from server.domain.dataformats.repositories import DataFormatRepository

from ..database import Database
from .transformers import make_entity, make_instance
from .models import DataFormatModel


class SqlDataFormatRepository(DataFormatRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def insert(self, entity: DataFormat) -> ID:
        async with self._db.session() as session:
            async with session.begin():

                instance = make_instance(entity)

                session.add(instance)

            await session.refresh(instance)

            return ID(instance.id)

    async def get_all(self, ids: List[ID] = None) -> List[DataFormat]:
        async with self._db.session() as session:
            stmt = select(DataFormatModel)
            if ids is not None:
                stmt = stmt.where(DataFormatModel.id.in_(ids))
            result = await session.execute(stmt)
            items = result.unique().scalars()
            return [make_entity(item) for item in items]
