import pytest
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from server.application.datasets.commands import DeleteDataset
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.infrastructure.database import Database
from server.infrastructure.datasets.models import DatasetModel
from server.infrastructure.tags.models import TagModel, dataset_tag
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory, CreateTagFactory


@pytest.mark.asyncio
async def test_dataset_cascades() -> None:
    bus = resolve(MessageBus)

    tag_id = await bus.execute(CreateTagFactory.build(name="Architecture"))
    dataset_id = await bus.execute(CreateDatasetFactory.build(tag_ids=[tag_id]))

    dataset = await bus.execute(GetDatasetByID(id=dataset_id))

    await bus.execute(DeleteDataset(id=dataset_id))

    # - Catalog record has been deleted.
    catalog_record_repository = resolve(CatalogRecordRepository)
    assert await catalog_record_repository.get_by_id(dataset.catalog_record.id) is None

    # - Tags have been disconnected from dataset, and still exist.
    async with resolve(Database).session() as session:
        stmt = (
            select(TagModel)
            .join(dataset_tag, isouter=True)
            .join(DatasetModel, isouter=True)
            .options(contains_eager(TagModel.datasets))
            .where(TagModel.id == tag_id)
        )
        result = await session.execute(stmt)
        tag = result.unique().scalar_one()
        assert tag.name == "Architecture"
        assert not tag.datasets
