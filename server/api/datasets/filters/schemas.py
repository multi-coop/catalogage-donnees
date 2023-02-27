from typing import Optional


class DatasetFiltersParams:
    def __init__(
        self,
        organization_id: Optional[str] = None,
    ) -> None:
        self.organization_id = organization_id
