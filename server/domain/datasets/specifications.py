from dataclasses import dataclass
from typing import Optional, Sequence


from server.domain.common.types import ID
from server.domain.extra_fields.entities import ExtraFieldValue
from server.domain.organizations.types import Siret


@dataclass(frozen=True)
class DatasetSpec:
    search_term: Optional[str] = None
    organization_siret: Optional[Siret] = None
    include_dataset_with_publication_restriction: Optional[bool] = True
    geographical_coverage__in: Optional[Sequence[str]] = None
    service__in: Optional[Sequence[str]] = None
    format__id__in: Optional[Sequence[Optional[int]]] = None
    technical_source__in: Optional[Sequence[str]] = None
    tag__id__in: Optional[Sequence[ID]] = None
    license: Optional[str] = None
    extra_field_value: Optional[ExtraFieldValue] = None
    include_all_datasets: bool = False
