import datetime as dt
import random
from typing import Any, TypeVar

import faker
from faker.providers import BaseProvider
from pydantic import BaseModel
from pydantic_factories import ModelFactory, Require, Use

from server.api.datasets.schemas import DatasetCreate, DatasetUpdate
from server.application.auth.commands import CreateDataPassUser, CreatePasswordUser
from server.application.datasets.commands import CreateDataset, UpdateDataset
from server.application.organizations.commands import CreateOrganization
from server.application.tags.commands import CreateTag
from server.domain.common import datetime as dtutil
from server.domain.datasets.entities import PublicationRestriction
from server.domain.licenses.entities import BUILTIN_LICENSE_SUGGESTIONS

T = TypeVar("T", bound=BaseModel)


class DateTimeTZProvider(BaseProvider):
    def date_time_tz(self) -> dt.datetime:
        return self.generator.date_time(dtutil.UTC)


fake = faker.Faker(["fr_FR"])
fake.add_provider(DateTimeTZProvider)


class Factory(ModelFactory[T]):
    __faker__ = fake

    @classmethod
    def get_mock_value(cls, field_type: Any) -> Any:
        if field_type is dt.datetime:
            return fake.date_time_tz()
        return super().get_mock_value(field_type)


class CreatePasswordUserFactory(Factory[CreatePasswordUser]):
    __model__ = CreatePasswordUser

    organization_siret = Require()


class CreateDataPassUserFactory(Factory[CreateDataPassUser]):
    __model__ = CreateDataPassUser


class CreateTagFactory(Factory[CreateTag]):
    __model__ = CreateTag


_FAKE_GEOGRAPHICAL_COVERAGES = [
    "Ville d'Angers",
    "Métropole Européenne de Lille",
    "Région Île-de-France",
    "Région Nouvelle-Aquitaine",
    "France métropolitaine",
    "Monde",
]


class _BaseCreateDatasetFactory:
    organization_siret = Require()
    title = Use(fake.sentence)
    description = Use(fake.text)
    service = Use(fake.company)
    geographical_coverage = Use(lambda: random.choice(_FAKE_GEOGRAPHICAL_COVERAGES))
    format_ids = Use(lambda: [random.randint(1, 6)])
    technical_source = Use(
        lambda: fake.sentence(nb_words=3) if random.random() < 0.5 else None
    )
    producer_email = Use(fake.ascii_free_email)
    contact_emails = Use(
        lambda: [fake.ascii_free_email() for _ in range(random.randint(1, 3))]
    )
    url = Use(lambda: fake.url() if random.random() < 0.5 else None)
    license = Use(random.choice, [None, *BUILTIN_LICENSE_SUGGESTIONS])
    tag_ids = Use(lambda: [])
    extra_field_values = Use(lambda: [])
    publication_restriction = PublicationRestriction.NO_RESTRICTION


class CreateDatasetFactory(_BaseCreateDatasetFactory, Factory[CreateDataset]):
    __model__ = CreateDataset

    account = Require()


class CreateDatasetPayloadFactory(_BaseCreateDatasetFactory, Factory[DatasetCreate]):
    __model__ = DatasetCreate


class _BaseUpdateDatasetFactory:
    tag_ids = Use(lambda: [])
    format_ids = Use(lambda: [1, 2])
    extra_field_values = Use(lambda: [])


class UpdateDatasetFactory(_BaseCreateDatasetFactory, Factory[UpdateDataset]):
    __model__ = UpdateDataset

    account = Require()


class UpdateDatasetPayloadFactory(_BaseUpdateDatasetFactory, Factory[DatasetUpdate]):
    __model__ = DatasetUpdate

    @classmethod
    def build_from_create_command(
        cls, command: CreateDataset, **kwargs: Any
    ) -> DatasetUpdate:
        return cls.build(
            **command.dict(exclude={"account", "organization_siret"}), **kwargs
        )


class CreateOrganizationFactory(Factory[CreateOrganization]):
    __model__ = CreateOrganization

    name = Use(fake.company)
    siret = Use(fake.siret)
    logo_url = None
