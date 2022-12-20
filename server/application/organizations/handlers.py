from server.application.organizations.commands import CreateOrganization
from server.application.organizations.queries import GetOrganizationBySiret
from server.config.di import resolve
from server.domain.organizations.entities import Organization
from server.domain.organizations.exceptions import (
    OrganizationAlreadyExists,
    OrganizationDoesNotExist,
)
from server.domain.organizations.repositories import OrganizationRepository
from server.domain.organizations.types import Siret

from .views import OrganizationView


async def get_organization_by_siret(query: GetOrganizationBySiret) -> OrganizationView:
    repository = resolve(OrganizationRepository)

    siret = query.siret
    organization = await repository.get_by_siret(siret)

    if organization is None:
        raise OrganizationDoesNotExist(siret)

    return OrganizationView(**organization.dict())


async def create_organization(command: CreateOrganization) -> Siret:
    repository = resolve(OrganizationRepository)

    organization = await repository.get_by_siret(command.siret)

    if organization is not None:
        raise OrganizationAlreadyExists(organization)

    organization = Organization(
        siret=command.siret, name=command.name, logo_url=command.logo_url
    )

    return await repository.insert(organization)
