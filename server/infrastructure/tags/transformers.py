from server.domain.tags.entities import Tag

from .models import TagModel


def make_entity(instance: TagModel) -> Tag:
    return Tag(**{field: getattr(instance, field) for field in Tag.__fields__})


def make_instance(entity: Tag) -> TagModel:
    return TagModel(**entity.dict())
