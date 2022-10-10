import httpx
import pytest

from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory
from ..helpers import TestPasswordUser


@pytest.mark.asyncio
async def test_license_list(
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    response = await client.get("/licenses/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == ["Licence Ouverte", "ODC Open Database License"]

    await bus.execute(
        CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            license="Autre licence",
        )
    )

    response = await client.get("/licenses/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == [
        "Autre licence",
        "Licence Ouverte",
        "ODC Open Database License",
    ]


@pytest.mark.asyncio
async def test_license_list_permissions(client: httpx.AsyncClient) -> None:
    response = await client.get("/licenses/")
    assert response.status_code == 401
