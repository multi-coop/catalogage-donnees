from typing import Optional

from server.seedwork.domain.entities import Entity


class DataFormat(Entity):
    id: Optional[int] = None
    name: str
