import logging
from typing import List

from fastapi import APIRouter, Depends

from server.application.dataformats.queries import GetAllDataFormat
from server.application.dataformats.views import DataFormatView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dataformat", tags=["dataformat"])


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=List[DataFormatView],
)
async def list_dataformat() -> List[DataFormatView]:

    bus = resolve(MessageBus)
    return await bus.execute(GetAllDataFormat())
