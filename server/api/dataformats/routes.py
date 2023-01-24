import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from server.api.dataformats.schemas import DataFormatCreate
from server.application.dataformats.commands import CreateDataFormat
from server.application.dataformats.exceptions import CannotCreateDataFormat
from server.application.dataformats.queries import GetAllDataFormat, GetDataFormatById
from server.application.dataformats.views import DataFormatView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dataformats", tags=["dataformat"])


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=List[DataFormatView],
)
async def list_dataformat() -> List[DataFormatView]:

    bus = resolve(MessageBus)
    return await bus.execute(GetAllDataFormat())


@router.post(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DataFormatView,
    status_code=201,
)
async def create_dataformat(data: DataFormatCreate) -> DataFormatView:
    bus = resolve(MessageBus)
    print(data)

    command = CreateDataFormat(value=data.value)

    try:
        id = await bus.execute(command)
        query = GetDataFormatById(id=id)
        return await bus.execute(query)

    except CannotCreateDataFormat as exc:
        logger.exception(exc)
        raise HTTPException(403, detail="Permission denied")
