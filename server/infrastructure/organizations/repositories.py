from typing import Optional, Set

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from server.domain.organizations.entities import Organization
from server.domain.organizations.repositories import OrganizationRepository
from server.domain.organizations.types import Siret

from ..database import Database
from .models import OrganizationModel
from .transformers import make_entity, make_instance


class SqlOrganizationRepository(OrganizationRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_by_siret(self, siret: Siret) -> Optional[Organization]:
        async with self._db.session() as session:
            stmt = select(OrganizationModel).where(OrganizationModel.siret == siret)
            result = await session.execute(stmt)
            try:
                instance = result.scalar_one()
            except NoResultFound:
                return None
            else:
                return make_entity(instance)

    async def get_siret_set(self) -> Set[Siret]:
        async with self._db.session() as session:
            stmt = select(OrganizationModel.siret.distinct())
            result = await session.execute(stmt)
            return {Siret(v) for v in result.scalars()}

    async def insert(self, entity: Organization) -> Siret:
        async with self._db.session() as session:
            instance = make_instance(entity)

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return instance.siret
