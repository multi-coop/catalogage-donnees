from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from server.domain.catalogs.entities import Catalog
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.organizations.types import Siret

from ..database import Database
from .models import CatalogModel
from .transformers import make_entity, make_instance


class SqlCatalogRepository(CatalogRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_siret(self, siret: Siret) -> Optional[Catalog]:
        async with self._db.session() as session:
            stmt = (
                select(CatalogModel)
                .join(CatalogModel.extra_fields, isouter=True)
                .options(contains_eager(CatalogModel.extra_fields))
                .where(CatalogModel.organization_siret == siret)
            )
            result = await session.execute(stmt)
            instance = result.unique().scalar_one_or_none()
            if instance is None:
                return None
            return make_entity(instance)

    async def insert(self, entity: Catalog) -> Siret:
        async with self._db.session() as session:
            instance = make_instance(entity)

            session.add(instance)
            session.add_all(instance.extra_fields)

            await session.commit()
            await session.refresh(instance)

            return instance.organization_siret
