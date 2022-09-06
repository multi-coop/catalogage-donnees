from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.common.types import ID

from .models import CatalogRecordModel


async def get_catalog_record_instance_by_id(
    session: AsyncSession, id_: ID
) -> CatalogRecordModel:
    stmt = select(CatalogRecordModel).where(CatalogRecordModel.id == id_)
    result = await session.execute(stmt)
    return result.scalar_one()
