import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.tags.queries import GetAllTags
from server.config.di import resolve
from server.domain.common.types import Skip
from server.seedwork.application.messages import MessageBus
from tools.remove_duplicated_tags import main

from ..factories import (
    CreateDatasetFactory,
    CreateOrganizationFactory,
    CreateTagFactory,
)


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

    await bus.execute(
        CreateDatasetFactory.build(
            account=Skip(),
            tag_ids=[tag_id_1, tag_id_2, tag_id_3],
            organization_siret=siret,
        )
    )

    await main()

    tags = await bus.execute(GetAllTags())

    assert len(tags) == 2
