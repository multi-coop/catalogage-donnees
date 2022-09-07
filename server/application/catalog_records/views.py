import datetime as dt

from pydantic import BaseModel

from server.domain.common.types import ID

from ..organizations.views import OrganizationView


class CatalogRecordView(BaseModel):
    id: ID
    organization: OrganizationView
    created_at: dt.datetime
