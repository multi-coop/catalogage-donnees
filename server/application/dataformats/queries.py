from typing import List

from server.seedwork.application.queries import Query

from .views import DataFormatView


class GetAllDataFormat(Query[List[DataFormatView]]):
    pass
