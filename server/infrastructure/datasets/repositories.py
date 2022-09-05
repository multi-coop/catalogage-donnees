from typing import List, Optional, Set, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from server.domain.common.pagination import Page
from server.domain.common.types import ID
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.domain.datasets.specifications import DatasetSpec

from ..catalog_records.models import CatalogRecordModel
from ..catalog_records.raw_queries import get_catalog_record_instance_by_id
from ..catalogs.models import CatalogModel
from ..database import Database
from ..helpers.sqlalchemy import get_count_from, to_limit_offset
from ..tags.raw_queries import get_all_tag_instances_by_ids
from .models import DatasetModel
from .queries.get_all import GetAllQuery
from .raw_queries import get_all_dataformat_instances
from .transformers import make_entity, make_instance, update_instance


class SqlDatasetRepository(DatasetRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_all(
        self,
        *,
        page: Page = Page(),
        spec: DatasetSpec = DatasetSpec(),
    ) -> Tuple[List[Tuple[Dataset, DatasetGetAllExtras]], int]:
        limit, offset = to_limit_offset(page)

        async with self._db.session() as session:
            query = GetAllQuery(spec)
            stmt = query.statement
            count = await get_count_from(stmt, session)
            result = await session.stream(stmt.limit(limit).offset(offset))
            items = [
                (make_entity(query.instance(row)), query.extras(row))
                async for row in result
            ]
            return items, count

    async def _maybe_get_by_id(
        self, session: AsyncSession, id: ID
    ) -> Optional[DatasetModel]:
        stmt = (
            select(DatasetModel)
            .join(DatasetModel.catalog_record)
            .join(CatalogRecordModel.catalog)
            .join(CatalogModel.organization)
            .where(DatasetModel.id == id)
            .options(
                contains_eager(DatasetModel.catalog_record)
                .contains_eager(CatalogRecordModel.catalog)
                .contains_eager(CatalogModel.organization),
                selectinload(DatasetModel.formats),
                selectinload(DatasetModel.tags),
                selectinload(DatasetModel.extra_field_values),
            )
        )
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return None

            return make_entity(instance)

    async def get_geographical_coverage_set(self) -> Set[str]:
        async with self._db.session() as session:
            stmt = select(DatasetModel.geographical_coverage.distinct())
            result = await session.execute(stmt)
            return set(result.scalars())

    async def get_service_set(self) -> Set[str]:
        async with self._db.session() as session:
            stmt = select(DatasetModel.service.distinct())
            result = await session.execute(stmt)
            return set(result.scalars())

    async def get_technical_source_set(self) -> Set[str]:
        async with self._db.session() as session:
            stmt = select(DatasetModel.technical_source.distinct()).where(
                DatasetModel.technical_source.is_not(None)
            )
            result = await session.execute(stmt)
            return set(result.scalars())

    async def get_license_set(self) -> Set[str]:
        async with self._db.session() as session:
            stmt = select(DatasetModel.license.distinct()).where(
                DatasetModel.license.is_not(None)
            )
            result = await session.execute(stmt)
            return set(result.scalars())

    async def insert(self, entity: Dataset) -> ID:
        async with self._db.session() as session:
            async with session.begin():
                catalog_record = await get_catalog_record_instance_by_id(
                    session, entity.catalog_record.id
                )
                formats = await get_all_dataformat_instances(session, entity.formats)
                tags = await get_all_tag_instances_by_ids(
                    session, [tag.id for tag in entity.tags]
                )
                instance = make_instance(entity, catalog_record, formats, tags)

                session.add(instance)

            await session.refresh(instance)

            return ID(instance.id)

    async def update(self, entity: Dataset) -> None:
        async with self._db.session() as session:
            async with session.begin():
                instance = await self._maybe_get_by_id(session, entity.id)

                if instance is None:
                    return

                formats = await get_all_dataformat_instances(session, entity.formats)
                tags = await get_all_tag_instances_by_ids(
                    session, [tag.id for tag in entity.tags]
                )
                update_instance(instance, entity, formats, tags)

    async def delete(self, id: ID) -> None:
        async with self._db.session() as session:
            instance = await self._maybe_get_by_id(session, id)

            if instance is None:
                return

            await session.delete(instance)

            await session.commit()
