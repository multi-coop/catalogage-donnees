from typing import List, Union

import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.datasets.queries import GetDatasetByID
from server.application.tags.queries import GetAllTags
from server.application.tags.views import TagView
from server.config.di import resolve
from server.domain.common.types import ID, Skip
from server.domain.datasets.repositories import DatasetGetAllExtras, DatasetRepository
from server.domain.tags.entities import Tag
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus
from tools.remove_duplicated_tags import (
    build_tag_table_of_truth,
    get_tags_to_delete_list,
    main,
    update_dataset_tags,
)

from ..factories import (
    CreateDatasetFactory,
    CreateOrganizationFactory,
    CreateTagFactory,
)


def get_tag_names(tags: List[TagView]) -> List[str]:
    return list(map(lambda x: x.name, tags))


def get_tag_ids(tags: Union[List[TagView], List[Tag]]) -> List[ID]:
    tags_ids = []
    for tag in tags:
        if tag.id is not None:
            tags_ids.append(tag.id)
    return tags_ids


@pytest.mark.asyncio
async def test_should_remove_links_between_duplicated_tags_and_dataset() -> None:

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
    assert set(get_tag_ids(dataset_1.tags)).issubset(set(get_tag_ids(tags)))

    assert "not_dulicated_tag" in get_tag_names(dataset_1.tags)

    dataset_2 = await bus.execute(GetDatasetByID(id=dataset_id_2, account=Skip()))
    assert len(dataset_2.tags) == 1

    # check  dataset_2 tag list contains only ids included in tag list
    assert set(get_tag_ids(dataset_2.tags)).issubset(set(get_tag_ids(tags)))


@pytest.mark.asyncio
async def test_dataset_should_have_only_tags_from_the_table_of_truth() -> None:

    bus = resolve(MessageBus)

    datset_repository = resolve(DatasetRepository)

    # Simulate an existing organization and catalog
    siret = await bus.execute(
        CreateOrganizationFactory.build(name="Ministère 1", siret="11004601800013")
    )
    await bus.execute(
        CreateCatalog(
            organization_siret=siret,
        )
    )

    tag_name = "services"

    tag_id_1 = await bus.execute(CreateTagFactory.build(name=tag_name))

    tag_id_2 = await bus.execute(CreateTagFactory.build(name="chemin de fer"))

    duplicated_tag_services_id = await bus.execute(
        CreateTagFactory.build(name=tag_name)
    )

    dataset_id = await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[duplicated_tag_services_id, tag_id_2],
            organization_siret=siret,
        )
    )

    dataset = await datset_repository.get_by_id(dataset_id)

    if dataset is None:
        return

    dataset_results = [
        (
            dataset,
            DatasetGetAllExtras(headlines={"title": "tata", "description": "toto"}),
        )
    ]

    tags_mapping = {dataset_id: [tag_id_1, tag_id_2]}

    await update_dataset_tags(dataset_results, dataset_ids_map=tags_mapping, bus=bus)

    dataset = await datset_repository.get_by_id(dataset_id)

    assert dataset is not None

    tags = dataset.tags

    tag_ids = get_tag_ids(tags)

    assert duplicated_tag_services_id not in tag_ids


@pytest.mark.asyncio
async def test_should_not_have_duplicated_tag_stored_1() -> None:

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

    tag_id_2 = await bus.execute(CreateTagFactory.build(name="not_used"))
    tag_id_3 = await bus.execute(CreateTagFactory.build(name="not_used"))
    tag_id_4 = await bus.execute(CreateTagFactory.build(name="tag-1"))

    await bus.execute(CreateTagFactory.build(name="tag-2"))
    await bus.execute(CreateTagFactory.build(name="not_used"))

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1, tag_id_2, tag_id_3],
            organization_siret=siret,
        )
    )

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_4],
            organization_siret=siret,
        )
    )

    await main()

    tags = await bus.execute(GetAllTags())

    tag_names = get_tag_names(tags)

    assert len(tag_names) == len(set(tag_names))


@pytest.mark.asyncio
async def test_should_not_have_duplicated_tag_stored_3() -> None:

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

    duplicated_tag = await bus.execute(CreateTagFactory.build(name=tag_name))

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[duplicated_tag],
            organization_siret=siret,
        )
    )

    await main()

    tags = await bus.execute(GetAllTags())

    tag_names = get_tag_names(tags)

    assert len(tag_names) == len(set(tag_names))


@pytest.mark.asyncio
async def test_build_tag_table_of_truth() -> None:
    bus = resolve(MessageBus)
    tag_respository = resolve(TagRepository)
    tag_name = "services"

    tag_id_1 = await bus.execute(CreateTagFactory.build(name=tag_name))

    duplicated_tag_id = await bus.execute(CreateTagFactory.build(name=tag_name))

    tag_id_2 = await bus.execute(CreateTagFactory.build(name="chemin de fer"))
    tag_id_3 = await bus.execute(CreateTagFactory.build(name="population"))
    tag_id_4 = await bus.execute(CreateTagFactory.build(name="écologie des sols"))
    tag_id_5 = await bus.execute(CreateTagFactory.build(name="environnement"))
    tag_id_7 = await bus.execute(CreateTagFactory.build(name="service des eaux"))
    tag_id_8 = await bus.execute(CreateTagFactory.build(name="sociologie de l'habitat"))

    expected_result = {
        tag_name: tag_id_1,
        "population": tag_id_3,
        "écologie des sols": tag_id_4,
        "service des eaux": tag_id_7,
        "environnement": tag_id_5,
        "chemin de fer": tag_id_2,
        "sociologie de l'habitat": tag_id_8,
    }

    tags = await tag_respository.get_all()

    result = build_tag_table_of_truth(tags)
    assert expected_result == result
    assert duplicated_tag_id not in result.values()


@pytest.mark.asyncio
async def test_should_not_have_duplicated_tag_stored_2() -> None:

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
    await bus.execute(CreateTagFactory.build(name=tag_name))

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1],
            organization_siret=siret,
        )
    )

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1],
            organization_siret=siret,
        )
    )

    await main()

    tags = await bus.execute(GetAllTags())

    tag_names = get_tag_names(tags)

    assert len(tag_names) == len(set(tag_names))


@pytest.mark.asyncio
async def test_get_tag_to_delete_list() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)
    tag_name = "services"

    tag_id_1 = await bus.execute(CreateTagFactory.build(name=tag_name))

    duplicated_tag_id = await bus.execute(CreateTagFactory.build(name=tag_name))

    tag_id_2 = await bus.execute(CreateTagFactory.build(name="chemin de fer"))
    tag_id_3 = await bus.execute(CreateTagFactory.build(name="population"))
    tag_id_4 = await bus.execute(CreateTagFactory.build(name="écologie des sols"))
    tag_id_5 = await bus.execute(CreateTagFactory.build(name="environnement"))
    tag_id_7 = await bus.execute(CreateTagFactory.build(name="service des eaux"))
    tag_id_8 = await bus.execute(CreateTagFactory.build(name="sociologie de l'habitat"))

    table_of_truth = {
        tag_name: tag_id_1,
        "population": tag_id_3,
        "écologie des sols": tag_id_4,
        "service des eaux": tag_id_7,
        "environnement": tag_id_5,
        "chemin de fer": tag_id_2,
        "sociologie de l'habitat": tag_id_8,
    }

    tags = await tag_repository.get_all()

    expected_result = [duplicated_tag_id]

    result = get_tags_to_delete_list(tags, table_of_truth)
    assert expected_result == result
