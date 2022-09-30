import pytest

from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.organizations.types import Siret
from server.infrastructure.catalogs.models import CatalogModel
from server.infrastructure.database import Database
from server.infrastructure.organizations.models import OrganizationModel
from server.seedwork.application.messages import MessageBus
from tests.helpers import create_test_password_user

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
    user = await create_test_password_user(
        CreatePasswordUserFactory.build(organization_siret=siret, email=email)
    )
    assert user.account.organization_siret == siret

    # Add a dataset to the catalog...
    dataset_id = await bus.execute(
        CreateDatasetFactory.build(account=user.account, organization_siret=siret)
    )

    dataset = await bus.execute(GetDatasetByID(id=dataset_id))
    assert dataset.catalog_record.organization.siret == siret
