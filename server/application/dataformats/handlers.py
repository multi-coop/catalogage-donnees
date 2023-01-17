from typing import List

from server.application.dataformats.queries import GetAllDataFormat
from server.application.dataformats.views import DataFormatView
from server.config.di import resolve
from server.domain.dataformats.repositories import DataFormatRepository


async def get_all_dataformats(query: GetAllDataFormat) -> List[DataFormatView]:
    repository = resolve(DataFormatRepository)
    dataformats = await repository.get_all()
    return [DataFormatView(**dataformat.dict()) for dataformat in dataformats]
