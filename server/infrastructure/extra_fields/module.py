from server.application.extra_fields.handlers import get_all_extra_fields
from server.application.extra_fields.queries import GetAllExtraFields
from server.seedwork.application.modules import Module


class ExtraFieldModule(Module):
    query_handlers = {GetAllExtraFields: get_all_extra_fields}
