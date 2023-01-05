from server.domain.dataformats.entities import DataFormat

from .models import DataFormatModel


def make_entity(instance: DataFormatModel) -> DataFormat:
    return DataFormat(name=instance.name, id=instance.id)


def make_instance(entity: DataFormat) -> DataFormatModel:
    return DataFormatModel(**entity.dict())
