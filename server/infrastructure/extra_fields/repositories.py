from typing import List

from sqlalchemy import select

from server.domain.extra_fields.entities import ExtraField
from server.domain.extra_fields.repositories import ExtraFieldRepository

from ..database import Database
from .models import ExtraFieldModel
from .transformers import make_entity


class SqlExtraFieldRepository(ExtraFieldRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_all(self, organization_siret: str) -> List[ExtraField]:
        async with self._db.session() as session:
            stmt = select(ExtraFieldModel).where(
                ExtraFieldModel.organization_siret == organization_siret
            )

            result = await session.execute(stmt)

            items = result.unique().scalars().all()

            return [make_entity(item) for item in items]
