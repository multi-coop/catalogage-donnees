import pytest

from server.application.datasets.queries import GetAllDatasets
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus
from tools import addrandomdatasets


@pytest.mark.asyncio
@pytest.mark.usefixtures("tags")
async def test_addrandomdatasets(temp_org: OrganizationView) -> None:
    bus = resolve(MessageBus)

    pagination = await bus.execute(GetAllDatasets())
    assert pagination.total_items == 0

    await addrandomdatasets.main(n=20, siret=temp_org.siret)

    pagination = await bus.execute(GetAllDatasets())
    assert pagination.total_items == 20
