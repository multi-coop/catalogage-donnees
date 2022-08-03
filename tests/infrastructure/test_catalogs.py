import pytest
from pydantic import EmailStr

from server.application.auth.queries import GetAccountByEmail
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.organizations.types import Siret
from server.infrastructure.catalogs.models import CatalogModel
from server.infrastructure.database import Database
from server.infrastructure.organizations.repositories import OrganizationModel
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory, CreatePasswordUserFactory


@pytest.mark.asyncio
async def test_catalog_creation_and_relationships() -> None:
    bus = resolve(MessageBus)
    db = resolve(Database)

    siret = Siret("123 456 789 12345")

    # Create an organization...
    async with db.session() as session:
        session.add(OrganizationModel(siret=siret, name="Example organization"))
        await session.commit()

    # And its catalog...
    async with db.session() as session:
        session.add(CatalogModel(organization_siret=siret))
        await session.commit()

    # Add a user to the organization...
    email = "test@mydomain.org"
    await bus.execute(
        CreatePasswordUserFactory.build(organization_siret=siret, email=email)
    )

    account = await bus.execute(GetAccountByEmail(email=EmailStr("test@mydomain.org")))
    assert account.organization_siret == siret

    # Add a dataset to the catalog...
    dataset_id = await bus.execute(CreateDatasetFactory.build(organization_siret=siret))

    dataset = await bus.execute(GetDatasetByID(id=dataset_id))
    assert dataset.catalog_record.organization_siret == siret
