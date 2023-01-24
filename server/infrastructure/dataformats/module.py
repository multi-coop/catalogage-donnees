from server.application.dataformats.commands import CreateDataFormat
from server.application.dataformats.handlers import (
    create_dataformat,
    get_all_dataformats,
    get_by_id,
)
from server.application.dataformats.queries import GetAllDataFormat, GetDataFormatById
from server.seedwork.application.modules import Module


class DataFormatModule(Module):
    query_handlers = {
        GetAllDataFormat: get_all_dataformats,
        GetDataFormatById: get_by_id,
    }
    command_handlers = {CreateDataFormat: create_dataformat}
