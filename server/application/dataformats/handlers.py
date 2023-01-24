from typing import List, Optional

from server.application.dataformats.commands import CreateDataFormat
from server.application.dataformats.queries import GetAllDataFormat, GetDataFormatById
from server.application.dataformats.views import DataFormatView
from server.config.di import resolve
from server.domain.dataformats.entities import DataFormat
from server.domain.dataformats.repositories import DataFormatRepository


async def get_all_dataformats(query: GetAllDataFormat) -> List[DataFormatView]:
    repository = resolve(DataFormatRepository)
    dataformats = await repository.get_all()
    return [DataFormatView(**dataformat.dict()) for dataformat in dataformats]


async def create_dataformat(command: CreateDataFormat) -> Optional[int]:
    repository = resolve(DataFormatRepository)
    return await repository.insert(DataFormat(name=command.value))


async def get_by_id(query: GetDataFormatById) -> Optional[DataFormatView]:
    repository = resolve(DataFormatRepository)
    dataformat = await repository.get_by_id(id=query.id)

    if dataformat is not None:
        return DataFormatView(**dataformat.dict())
    return None
