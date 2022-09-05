from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.common.types import ID

from .models import TagModel


async def get_all_tag_instances_by_ids(
    session: AsyncSession, ids: List[ID]
) -> List[TagModel]:
    stmt = select(TagModel).where(TagModel.id.in_(ids))
    result = await session.execute(stmt)
    return result.scalars().all()
