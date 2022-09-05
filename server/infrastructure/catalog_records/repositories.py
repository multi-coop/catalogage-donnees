from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from server.domain.catalog_records.entities import CatalogRecord
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.common.types import ID

from ..catalogs.models import CatalogModel
from ..database import Database
from .models import CatalogRecordModel
from .transformers import make_entity, make_instance


class SqlCatalogRecordRepository(CatalogRecordRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_id(self, id: ID) -> Optional[CatalogRecord]:
        async with self._db.session() as session:
            stmt = (
                select(CatalogRecordModel)
                .join(CatalogRecordModel.catalog)
                .join(CatalogModel.organization)
                .options(
                    contains_eager(CatalogRecordModel.catalog).contains_eager(
                        CatalogModel.organization
                    )
                )
                .where(CatalogRecordModel.id == id)
            )
            result = await session.execute(stmt)
            instance = result.scalar_one_or_none()
            if instance is None:
                return None
            return make_entity(instance)

    async def insert(self, entity: CatalogRecord) -> ID:
        async with self._db.session() as session:
            instance = make_instance(entity)

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return ID(instance.id)
