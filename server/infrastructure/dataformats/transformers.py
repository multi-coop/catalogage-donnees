from server.domain.dataformats.entities import DataFormat

from .models import DataFormatModel


def make_entity(instance: DataFormatModel) -> DataFormat:
    return DataFormat(
        **{field: getattr(instance, field) for field in DataFormat.__fields__}
    )


def make_instance(entity: DataFormat) -> DataFormatModel:
    return DataFormatModel(**entity.dict())
