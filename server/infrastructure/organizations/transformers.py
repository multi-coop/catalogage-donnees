from server.domain.organizations.entities import Organization

from .models import OrganizationModel


def make_entity(instance: OrganizationModel) -> Organization:
    return Organization(
        siret=instance.siret, name=instance.name, logo_url=instance.logo_url
    )


def make_instance(entity: Organization) -> OrganizationModel:
    return OrganizationModel(**entity.dict())
