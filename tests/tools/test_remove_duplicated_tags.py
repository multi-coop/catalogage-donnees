import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.datasets.queries import GetDatasetByID
from server.application.tags.queries import GetAllTags
from server.config.di import resolve
from server.domain.common.types import Skip
from server.domain.datasets.entities import DataFormat, Dataset
from server.domain.datasets.repositories import DatasetRepository
from server.domain.tags.entities import Tag
from server.seedwork.application.messages import MessageBus
from tools.remove_duplicated_tags import link_dataset_with_tags_to_keep, main

from ..factories import (
    CreateDatasetFactory,
    CreateOrganizationFactory,
    CreateTagFactory,
    _BaseCreateDatasetFactory,
)


@pytest.mark.asyncio
async def test_link_dataset_with_tags_to_keep() -> None:

    # Duplicated tags
    tag_name="duplicated-tad"


    bus = resolve(MessageBus)
    dataset_repository = resolve(DatasetRepository)

    # Simulate an existing organization and catalog
    siret = await bus.execute(
        CreateOrganizationFactory.build(name="Ministère 1", siret="11004601800013")
    )

    await bus.execute(
        CreateCatalog(
            organization_siret=siret,
        )
    )

    tag_id_1 = await bus.execute(CreateTagFactory.build(name=tag_name))
    tag_id_2 = await bus.execute(CreateTagFactory.build(name=tag_name))


    # # Not duplicated tag

    tag_id_3 = await bus.execute(CreateTagFactory.build(name="not_dulicated_tag"))


    dataset_id_1 = await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1, tag_id_2, tag_id_3],
            organization_siret=siret,
        )
    )

    dataset_1 = await dataset_repository.get_by_id(id=dataset_id_1)

    dataset_results = [(dataset_1, None)]


    table_of_truth = {tag_name: tag_id_1, "not_dulicated_tag":tag_id_3 }

    result = link_dataset_with_tags_to_keep(
        dataset_results=dataset_results, table_of_truth=table_of_truth
    )

    expected_result = {
    dataset_id_1 : [tag_id_1, tag_id_3]
   }

    print(expected_result)
    print(result)

    assert result == expected_result



@pytest.mark.asyncio
async def test_remove_duplicated_tags() -> None:

    bus = resolve(MessageBus)

    # Simulate an existing organization and catalog
    siret = await bus.execute(
        CreateOrganizationFactory.build(name="Ministère 1", siret="11004601800013")
    )
    await bus.execute(
        CreateCatalog(
            organization_siret=siret,
        )
    )

    tag_name = "duplicated_tag"

    tag_id_1 = await bus.execute(CreateTagFactory.build(name=tag_name))
    tag_id_2 = await bus.execute(CreateTagFactory.build(name=tag_name))
    tag_id_3 = await bus.execute(CreateTagFactory.build(name="not_dulicated_tag"))

    dataset_id_1 = await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1, tag_id_2, tag_id_3],
            organization_siret=siret,
        )
    )

    dataset_id_2 = await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_2],
            organization_siret=siret,
        )
    )

    await main()

    tags = await bus.execute(GetAllTags())
    assert len(tags) == 2

    dataset_1 = await bus.execute(GetDatasetByID(id=dataset_id_1))
    assert len(dataset_1.tags) == 2

    dataset_2 = await bus.execute(GetDatasetByID(id=dataset_id_2))
    assert len(dataset_2.tags) == 1
    assert dataset_2.tags[0].id == tag_id_1
