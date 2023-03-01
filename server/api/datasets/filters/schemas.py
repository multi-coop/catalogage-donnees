from typing import Optional


class DatasetFiltersParams:
    def __init__(
        self,
        organization_siret: Optional[str] = None,
    ) -> None:
        self.organization_siret = organization_siret
