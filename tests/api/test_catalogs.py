import httpx
import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory, CreateOrganizationFactory
from ..helpers import TestPasswordUser, api_key_auth


@pytest.mark.asyncio
async def test_catalog_create(client: httpx.AsyncClient) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build())

    response = await client.post(
        "/catalogs/", json={"organization_siret": str(siret)}, auth=api_key_auth
    )
    assert response.status_code == 201
    assert response.json() == {
        "organization_siret": str(siret),
    }
    catalog = await bus.execute(GetCatalogBySiret(siret=siret))
    assert catalog.organization_siret == siret

    dataset_id = await bus.execute(CreateDatasetFactory.build(organization_siret=siret))
    dataset = await bus.execute(GetDatasetByID(id=dataset_id))
    assert dataset.catalog_record.organization_siret == siret


@pytest.mark.asyncio
async def test_catalog_create_already_exists(client: httpx.AsyncClient) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build())
    await bus.execute(CreateCatalog(organization_siret=siret))

    response = await client.post(
        "/catalogs/", json={"organization_siret": str(siret)}, auth=api_key_auth
    )
    assert response.status_code == 200
    assert response.json() == {
        "organization_siret": str(siret),
    }


@pytest.mark.asyncio
class TestCatalogPermissions:
    async def test_create_anonymous(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())
        response = await client.post(
            "/catalogs/", json={"organization_siret": str(siret)}
        )
        assert response.status_code == 403

    async def test_create_authenticated(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())
        response = await client.post(
            "/catalogs/", json={"organization_siret": str(siret)}, auth=temp_user.auth
        )
        assert response.status_code == 403
