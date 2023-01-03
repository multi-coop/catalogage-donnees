from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DataFormatModel


async def get_all_dataformat_instances(
    session: AsyncSession,
    formats: List[str],
) -> List[DataFormatModel]:
    stmt = select(DataFormatModel).where(DataFormatModel.name.in_(formats))
    result = await session.execute(stmt)
    return result.scalars().all()
