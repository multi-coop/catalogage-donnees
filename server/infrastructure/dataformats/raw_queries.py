from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DataFormatModel


async def get_all_dataformat_instances_by_ids(
    session: AsyncSession,
    ids: List[Optional[int]],
) -> List[DataFormatModel]:
    stmt = select(DataFormatModel).where(DataFormatModel.id.in_(ids))

    result = await session.execute(stmt)
    return result.scalars().all()
