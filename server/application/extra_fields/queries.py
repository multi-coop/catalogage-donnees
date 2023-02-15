from typing import List

from server.application.extra_fields.validation import GetCatalogExtraFields
from server.application.extra_fields.views import ExtraFieldView
from server.seedwork.application.queries import Query


class GetAllExtraFields(GetCatalogExtraFields, Query[List[ExtraFieldView]]):
    organization_id: str
