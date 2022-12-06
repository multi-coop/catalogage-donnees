from typing import List

import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.datasets.queries import GetDatasetByID
from server.application.tags.queries import GetAllTags
from server.application.tags.views import TagView
from server.config.di import resolve
from server.domain.common.types import ID, Skip
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.seedwork.application.messages import MessageBus
from tools.remove_duplicated_tags import link_dataset_with_tags_to_keep, main

from ..factories import (
    CreateDatasetFactory,
    CreateOrganizationFactory,
    CreateTagFactory,
)


@pytest.mark.asyncio
async def test_link_dataset_with_tags_to_keep() -> None:

    # Duplicated tags
    tag_name = "duplicated-tad"

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

    # Not duplicated tag

    tag_id_3 = await bus.execute(CreateTagFactory.build(name="not_dulicated_tag"))

    dataset_id_1 = await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1, tag_id_2, tag_id_3],
            organization_siret=siret,
        )
    )

    dataset_1 = await dataset_repository.get_by_id(id=dataset_id_1)

    if dataset_1 is None:
        return

    dataset_results = [
        (
            dataset_1,
            DatasetGetAllExtras(headlines={"title": "tata", "description": "toto"}),
        )
    ]

    table_of_truth = {tag_name: tag_id_1, "not_dulicated_tag": tag_id_3}

    result = link_dataset_with_tags_to_keep(
        dataset_results=dataset_results, table_of_truth=table_of_truth
    )

    expected_result = {dataset_id_1: [tag_id_1, tag_id_3]}

    assert result == expected_result


@pytest.mark.asyncio
async def test_remove_duplicated_tags() -> None:
    def get_tag_names(tags: List[TagView]) -> List[str]:
        return list(map(lambda x: x.name, tags))

    def get_tag_id(tags: List[TagView]) -> List[ID]:
        return list(map(lambda x: x.id, tags))

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
    tag_names = get_tag_names(tags)

    # check tag list has no tags with the same name
    assert len(tag_names) == len(set(tag_names))

    dataset_1 = await bus.execute(GetDatasetByID(id=dataset_id_1, account=Skip()))

    assert len(dataset_1.tags) == 2

    # check  dataset_1 tag list contains only ids included in tag list
    assert set(get_tag_id(dataset_1.tags)).issubset(set(get_tag_id(tags)))

    assert "not_dulicated_tag" in get_tag_names(dataset_1.tags)

    dataset_2 = await bus.execute(GetDatasetByID(id=dataset_id_2, account=Skip()))
    assert len(dataset_2.tags) == 1

    # check  dataset_2 tag list contains only ids included in tag list
    assert set(get_tag_id(dataset_2.tags)).issubset(set(get_tag_id(tags)))
