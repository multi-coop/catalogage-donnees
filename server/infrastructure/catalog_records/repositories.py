from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from server.domain.catalog_records.entities import CatalogRecord
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.common.types import ID

from ..database import Database
from .models import CatalogRecordModel
from .transformers import make_entity, make_instance


class SqlCatalogRecordRepository(CatalogRecordRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_id(self, id: ID) -> Optional[CatalogRecord]:
        async with self._db.session() as session:
            stmt = select(CatalogRecordModel).where(CatalogRecordModel.id == id)
            result = await session.execute(stmt)
            try:
                instance = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return make_entity(instance)

    async def insert(self, entity: CatalogRecord) -> ID:
        async with self._db.session() as session:
            instance = make_instance(entity)

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)
