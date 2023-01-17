from server.application.dataformats.handlers import get_all_dataformats
from server.application.dataformats.queries import GetAllDataFormat
from server.seedwork.application.modules import Module


class DataFormatModule(Module):
    query_handlers = {GetAllDataFormat: get_all_dataformats}
