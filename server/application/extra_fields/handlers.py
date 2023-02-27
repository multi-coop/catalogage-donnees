from typing import List

from server.application.extra_fields.queries import GetAllExtraFields
from server.application.extra_fields.views import ExtraFieldView
from server.config.di import resolve
from server.domain.extra_fields.repositories import ExtraFieldRepository


async def get_all_extra_fields(query: GetAllExtraFields) -> List[ExtraFieldView]:
    repository = resolve(ExtraFieldRepository)
    extra_fields = await repository.get_all(query.organization_id)

    return [
        ExtraFieldView(
            name=extra_field.name,
            title=extra_field.title,
            id=extra_field.id,
            organization_siret=extra_field.organization_siret,
            data=extra_field.data,
            hint_text=extra_field.hint_text,
            type=extra_field.type,
        )
        for extra_field in extra_fields
    ]
