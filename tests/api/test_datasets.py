import json
import random
from typing import Any, List, Tuple

import httpx
import pytest
from sqlalchemy import select

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret
from server.application.dataformats.views import DataFormatView
from server.application.datasets.queries import GetDatasetByID
from server.application.organizations.views import OrganizationView
from server.application.tags.commands import CreateTag
from server.application.tags.queries import GetTagByID
from server.config.di import resolve
from server.domain.common.types import ID, Skip, id_factory
from server.domain.dataformats.entities import DataFormat
from server.domain.dataformats.repositories import DataFormatRepository
from server.domain.datasets.entities import PublicationRestriction, UpdateFrequency
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.extra_fields.entities import (
    BoolExtraField,
    ExtraField,
    ExtraFieldValue,
    TextExtraField,
)
from server.domain.organizations.types import Siret
from server.infrastructure.database import Database
from server.infrastructure.extra_fields.models import ExtraFieldValueModel
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateDatasetFactory

from ..factories import (
    CreateDatasetPayloadFactory,
    CreateOrganizationFactory,
    CreatePasswordUserFactory,
    UpdateDatasetPayloadFactory,
    fake,
)
from ..helpers import TestPasswordUser, create_test_password_user, to_payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {"loc": ["body", "title"], "type": "value_error.missing"},
                {"loc": ["body", "description"], "type": "value_error.missing"},
                {"loc": ["body", "service"], "type": "value_error.missing"},
                {
                    "loc": ["body", "geographical_coverage"],
                    "type": "value_error.missing",
                },
                {"loc": ["body", "format_ids"], "type": "value_error.missing"},
                {"loc": ["body", "contact_emails"], "type": "value_error.missing"},
            ],
            id="missing-fields",
        ),
        pytest.param(
            {
                "title": "Title",
                "description": "Description",
                "service": "Service",
                "geographical_coverage": "national",
                "format_ids": [],
                "contact_emails": ["person@mydomain.org"],
            },
            [
                {
                    "loc": ["body", "format_ids"],
                    "msg": "formats must contain at least one item",
                }
            ],
            id="formats-empty",
        ),
        pytest.param(
            {
                "title": "Title",
                "description": "Description",
                "service": "Service",
                "geographical_coverage": "national",
                "format_ids": [1, 2],
                "contact_emails": [],
            },
            [
                {
                    "loc": ["body", "contact_emails"],
                    "msg": "contact_emails must contain at least one item",
                }
            ],
            id="contact_emails-empty",
        ),
    ],
)
async def test_create_dataset_invalid(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    payload: dict,
    expected_errors_attrs: list,
) -> None:
    payload = {"organization_siret": str(temp_org.siret), **payload}

    response = await client.post("/datasets/", json=payload, auth=temp_user.auth)
    assert response.status_code == 422

    data = response.json()
    assert len(data["detail"]) == len(expected_errors_attrs), data["detail"]

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_dataset_invalid_catalog_does_not_exist(
    client: httpx.AsyncClient,
) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build())
    # Catalog not created...
    user = await create_test_password_user(
        CreatePasswordUserFactory.build(organization_siret=siret)
    )

    payload = to_payload(CreateDatasetPayloadFactory.build(organization_siret=siret))
    response = await client.post("/datasets/", json=payload, auth=user.auth)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == f"Catalog not found: '{siret}'"


@pytest.mark.asyncio
async def test_dataset_crud(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    admin_user: TestPasswordUser,
) -> None:
    last_updated_at = fake.date_time_tz()

    dataformat_repository = resolve(DataFormatRepository)

    await dataformat_repository.insert(DataFormat(name="feuille de pappier"))

    payload = to_payload(
        CreateDatasetPayloadFactory.build(
            organization_siret=temp_org.siret,
            title="Example title",
            description="Example description",
            service="Example service",
            geographical_coverage="France métropolitaine",
            format_ids=[1, 2],
            technical_source="Example database",
            producer_email="example.service@mydomain.org",
            contact_emails=["example.person@mydomain.org"],
            update_frequency=UpdateFrequency.WEEKLY,
            last_updated_at=last_updated_at,
            url=None,
            license="Licence Ouverte",
            tag_ids=[],
        )
    )

    response = await client.post("/datasets/", json=payload, auth=temp_user.auth)
    assert response.status_code == 201
    data = response.json()

    pk = data["id"]
    assert isinstance(pk, str)

    assert data == {
        "id": pk,
        "catalog_record": {
            **data["catalog_record"],
            "organization": temp_org.dict(),
        },
        "title": "Example title",
        "description": "Example description",
        "service": "Example service",
        "geographical_coverage": "France métropolitaine",
        "formats": [
            DataFormatView(id=1, name="Fichier tabulaire (XLS, XLSX, CSV, ...)"),
            DataFormatView(id=2, name="Fichier SIG (Shapefile, ...)"),
        ],
        "technical_source": "Example database",
        "producer_email": "example.service@mydomain.org",
        "contact_emails": ["example.person@mydomain.org"],
        "update_frequency": "weekly",
        "last_updated_at": last_updated_at.isoformat(),
        "url": None,
        "license": "Licence Ouverte",
        "tags": [],
        "extra_field_values": [],
        "headlines": None,
        "publication_restriction": PublicationRestriction.NO_RESTRICTION.value,
    }

    non_existing_id = id_factory()

    response = await client.get(f"/datasets/{non_existing_id}/", auth=temp_user.auth)
    assert response.status_code == 404

    response = await client.get(f"/datasets/{pk}/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == data

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json()["items"] == [data]

    response = await client.delete(f"/datasets/{pk}/", auth=admin_user.auth)
    assert response.status_code == 204

    response = await client.get(f"/datasets/{pk}/", auth=temp_user.auth)
    assert response.status_code == 404

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json()["items"] == []


@pytest.mark.asyncio
class TestDatasetPermissions:
    async def test_create_not_authenticated(
        self, temp_org: OrganizationView, client: httpx.AsyncClient
    ) -> None:
        response = await client.post(
            "/datasets/",
            json=to_payload(
                CreateDatasetPayloadFactory.build(organization_siret=temp_org.siret)
            ),
        )
        assert response.status_code == 401

    async def test_create_in_other_org_denied(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)

        other_org_siret = await bus.execute(CreateOrganizationFactory.build())
        await bus.execute(CreateCatalog(organization_siret=other_org_siret))

        payload = to_payload(
            CreateDatasetPayloadFactory.build(organization_siret=other_org_siret)
        )
        response = await client.post("/datasets/", json=payload, auth=temp_user.auth)

        assert response.status_code == 403

    async def test_create_in_other_org_admin_denied(
        self, client: httpx.AsyncClient, admin_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)

        other_org_siret = await bus.execute(CreateOrganizationFactory.build())
        assert other_org_siret != admin_user.account.organization_siret
        await bus.execute(CreateCatalog(organization_siret=other_org_siret))

        payload = to_payload(
            CreateDatasetPayloadFactory.build(organization_siret=other_org_siret)
        )
        response = await client.post("/datasets/", json=payload, auth=admin_user.auth)
        assert response.status_code == 403

    async def test_get_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.get(f"/datasets/{pk}/")
        assert response.status_code == 401

    async def test_list_not_authenticated(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/datasets/")
        assert response.status_code == 401

    async def test_update_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.put(f"/datasets/{pk}/", json={})
        assert response.status_code == 401

    async def test_update_in_other_org_denied(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)

        other_org_siret = await bus.execute(CreateOrganizationFactory.build())
        await bus.execute(CreateCatalog(organization_siret=other_org_siret))

        command = CreateDatasetFactory.build(
            organization_siret=other_org_siret, account=Skip()
        )
        dataset_id = await bus.execute(command)

        payload = to_payload(
            UpdateDatasetPayloadFactory.build_from_create_command(command)
        )
        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=temp_user.auth
        )

        assert response.status_code == 403

    async def test_update_in_other_org_admin_denied(
        self, client: httpx.AsyncClient, admin_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)

        other_org_siret = await bus.execute(CreateOrganizationFactory.build())
        assert admin_user.account.organization_siret != other_org_siret
        await bus.execute(CreateCatalog(organization_siret=other_org_siret))

        command = CreateDatasetFactory.build(
            organization_siret=other_org_siret, account=Skip()
        )
        dataset_id = await bus.execute(command)

        payload = to_payload(
            UpdateDatasetPayloadFactory.build_from_create_command(command)
        )
        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=admin_user.auth
        )

        assert response.status_code == 403

    async def test_delete_not_authenticated(self, client: httpx.AsyncClient) -> None:
        pk = id_factory()
        response = await client.delete(f"/datasets/{pk}/")
        assert response.status_code == 401

    async def test_delete_not_admin(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        pk = id_factory()
        response = await client.delete(f"/datasets/{pk}/", auth=temp_user.auth)
        assert response.status_code == 403

    async def test_can_no_see_dataset_of_other_organizations_with_restricted_publication(  # noqa: E501
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
    ) -> None:

        bus = resolve(MessageBus)
        command = CreateDatasetFactory.build(
            organization_siret=temp_org.siret,
            publication_restriction=PublicationRestriction.DRAFT,
            account=Skip(),
        )
        dataset_id = await bus.execute(command)

        siret = await bus.execute(CreateOrganizationFactory.build())

        user = await create_test_password_user(
            CreatePasswordUserFactory.build(organization_siret=siret)
        )

        response = await client.get(f"/datasets/{dataset_id}/", auth=user.auth)

        assert response.status_code == 403

    async def test_can_see_dataset_of_other_organizations_without_publication_restriction(  # noqa: E501
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:

        bus = resolve(MessageBus)
        command = CreateDatasetFactory.build(
            organization_siret=temp_org.siret,
            publication_restriction=PublicationRestriction.NO_RESTRICTION,
            account=Skip(),
        )
        dataset_id = await bus.execute(command)

        siret = await bus.execute(CreateOrganizationFactory.build())

        user = await create_test_password_user(
            CreatePasswordUserFactory.build(organization_siret=siret)
        )

        response = await client.get(f"/datasets/{dataset_id}/", auth=user.auth)

        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, expected_total_pages, expected_num_items, expected_dataset_titles",
    [
        pytest.param(
            {},
            2,
            10,
            ["__skip__"],
            id="default",
        ),
        pytest.param(
            {"page_size": 3},
            5,
            3,
            ["Dataset 13", "Dataset 12", "Dataset 11"],
            id="first-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 4},
            5,
            3,
            ["Dataset 4", "Dataset 3", "Dataset 2"],
            id="some-middle-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 5},
            5,
            1,
            ["Dataset 1"],
            id="last-page",
        ),
        pytest.param(
            {"page_size": 3, "page_number": 6},
            5,
            0,
            [],
            id="beyond-last-page",
        ),
    ],
)
async def test_dataset_pagination(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    tags: list,
    params: dict,
    expected_total_pages: int,
    expected_num_items: int,
    expected_dataset_titles: List[str],
) -> None:
    bus = resolve(MessageBus)

    n_datasets = 13
    for k in range(1, n_datasets + 1):
        tag_ids = [tag.id for tag in random.choices(tags, k=random.randint(0, 2))]
        await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account,
                organization_siret=temp_org.siret,
                title=f"Dataset {k}",
                tag_ids=tag_ids,
                publication_restriction=PublicationRestriction.NO_RESTRICTION,
            )
        )

    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) == expected_num_items
    assert data["total_items"] == n_datasets
    assert data["page_size"] == params.get("page_size", 10)
    if "__skip__" not in expected_dataset_titles:
        assert [item["title"] for item in data["items"]] == expected_dataset_titles
    assert data["total_pages"] == expected_total_pages


@pytest.mark.asyncio
async def test_dataset_get_all_uses_reverse_chronological_order(  # noqa: E501
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    for title in ("Oldest", "Intermediate", "Newest"):
        await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account,
                organization_siret=temp_org.siret,
                title=title,
            )
        )

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    titles = [dataset["title"] for dataset in response.json()["items"]]
    assert titles == ["Newest", "Intermediate", "Oldest"]


@pytest.mark.asyncio
async def test_get_datasets_without_publication_restriction(
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    siret = await bus.execute(CreateOrganizationFactory.build())

    user = await create_test_password_user(
        CreatePasswordUserFactory.build(organization_siret=siret)
    )

    for publication_restriction in (
        PublicationRestriction.DRAFT,
        PublicationRestriction.LEGAL_RESTRICTION,
        PublicationRestriction.NO_RESTRICTION,
    ):
        await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account,
                organization_siret=temp_org.siret,
                title=f"Title {publication_restriction}",
                publication_restriction=publication_restriction,
            )
        )

    response = await client.get("/datasets/", auth=user.auth)
    assert response.status_code == 200
    publication_restriction_data = [
        dataset["publication_restriction"] for dataset in response.json()["items"]
    ]

    assert not set(
        [
            PublicationRestriction.LEGAL_RESTRICTION.value,
            PublicationRestriction.DRAFT.value,
        ]
    ).issubset(set(publication_restriction_data))
    assert PublicationRestriction.NO_RESTRICTION.value in publication_restriction_data


@pytest.mark.asyncio
async def test_get_datasets_with_publications_restrictions_of_my_organization_only_including_those_without_publication_restriction(  # noqa: E501
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    for publication_restriction in (
        PublicationRestriction.DRAFT,
        PublicationRestriction.LEGAL_RESTRICTION,
        PublicationRestriction.NO_RESTRICTION,
    ):
        await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account,
                organization_siret=temp_org.siret,
                title=f"Title {publication_restriction}",
                publication_restriction=publication_restriction,
            )
        )

    response = await client.get("/datasets/", auth=temp_user.auth)
    assert response.status_code == 200
    publication_restriction_data = [
        dataset["publication_restriction"] for dataset in response.json()["items"]
    ]

    assert set(
        [
            PublicationRestriction.LEGAL_RESTRICTION.value,
            PublicationRestriction.DRAFT.value,
            PublicationRestriction.NO_RESTRICTION.value,
        ]
    ).issubset(set(publication_restriction_data))


@pytest.mark.asyncio
class TestDatasetOptionalFields:
    @pytest.mark.parametrize(
        "field, default",
        [
            pytest.param("technical_source", None),
            pytest.param("producer_email", None),
            pytest.param("update_frequency", None),
            pytest.param("last_updated_at", None),
            pytest.param("license", None),
        ],
    )
    async def test_optional_fields_missing_uses_defaults(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
        field: str,
        default: Any,
    ) -> None:
        payload = to_payload(
            CreateDatasetFactory.build(
                account=temp_user.account, organization_siret=temp_org.siret
            )
        )
        payload.pop(field)
        response = await client.post("/datasets/", json=payload, auth=temp_user.auth)
        assert response.status_code == 201
        dataset = response.json()
        assert dataset[field] == default

    async def test_optional_fields_invalid(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        response = await client.post(
            "/datasets/",
            json={
                **to_payload(
                    CreateDatasetFactory.build(
                        account=temp_user.account, organization_siret=temp_org.siret
                    )
                ),
                "contact_emails": ["notanemail", "valid@mydomain.org"],
                "update_frequency": "not_in_enum",
                "last_updated_at": "not_a_datetime",
            },
            auth=temp_user.auth,
        )
        assert response.status_code == 422
        (
            err_contact_emails,
            err_update_frequency,
            err_last_updated_at,
        ) = response.json()["detail"]
        assert err_contact_emails["loc"] == ["body", "contact_emails", 0]
        assert err_contact_emails["type"] == "value_error.email"
        assert err_update_frequency["loc"] == ["body", "update_frequency"]
        assert err_update_frequency["type"] == "type_error.enum"
        assert err_last_updated_at["loc"] == ["body", "last_updated_at"]
        assert err_last_updated_at["type"] == "value_error.datetime"


@pytest.mark.asyncio
class TestDatasetUpdate:
    async def test_not_found(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        pk = id_factory()
        response = await client.put(
            f"/datasets/{pk}/",
            json=to_payload(UpdateDatasetPayloadFactory.build(id=pk)),
            auth=temp_user.auth,
        )
        assert response.status_code == 404

    async def test_full_entity_expected(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account, organization_siret=temp_org.siret
            )
        )

        # Apply PUT semantics, which expect a full entity.
        response = await client.put(
            f"/datasets/{dataset_id}/", json={}, auth=temp_user.auth
        )
        assert response.status_code == 422
        fields = [
            "title",
            "description",
            "service",
            "geographical_coverage",
            "format_ids",
            "technical_source",
            "producer_email",
            "contact_emails",
            "update_frequency",
            "last_updated_at",
            "url",
            "license",
            "tag_ids",
            "publication_restriction"
            # extra_field_values -- empty OK until frontend is implemented
        ]
        errors = response.json()["detail"]
        assert len(errors) == len(fields)
        for field, error in zip(fields, errors):
            assert error["loc"] == ["body", field], field
            assert error["type"] == "value_error.missing", field

    async def test_fields_empty_invalid(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)

        last_updated_at = fake.date_time_tz()
        command = CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            last_updated_at=last_updated_at,
        )

        dataset_id = await bus.execute(command)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json=to_payload(
                UpdateDatasetPayloadFactory.build_from_create_command(
                    command.copy(exclude={"title", "description", "service", "url"}),
                    factory_use_construct=True,  # Skip validation
                    title="",
                    description="",
                    service="",
                    url="",
                )
            ),
            auth=temp_user.auth,
        )
        assert response.status_code == 422

        (
            err_title,
            err_description,
            err_service,
            err_url,
        ) = response.json()["detail"]

        assert err_title["loc"] == ["body", "title"]
        assert "empty" in err_title["msg"]

        assert err_description["loc"] == ["body", "description"]
        assert "empty" in err_description["msg"]

        assert err_service["loc"] == ["body", "service"]
        assert "empty" in err_service["msg"]

        assert err_url["loc"] == ["body", "url"]
        assert "empty" in err_service["msg"]

    async def test_update_1(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)
        dataset_id = await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account, organization_siret=temp_org.siret
            )
        )

        other_last_updated_at = fake.date_time_tz()

        payload = to_payload(
            UpdateDatasetPayloadFactory.build(
                title="Other title",
                description="Other description",
                service="Other service",
                geographical_coverage="Hauts-de-France",
                format_ids=[1],
                technical_source="Other information system",
                producer_email="other.service@mydomain.org",
                contact_emails=["other.person@mydomain.org"],
                update_frequency=UpdateFrequency.WEEKLY,
                last_updated_at=other_last_updated_at.isoformat(),
                url="https://data.gouv.fr/datasets/other",
                license="ODC Open Database License",
                tag_ids=[],
                extra_field_values=[],
                publication_restriction=PublicationRestriction.LEGAL_RESTRICTION,
            )
        )

        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=temp_user.auth
        )
        assert response.status_code == 200

        # API (REST, GraphQL, ...) returns updated representation
        data = response.json()
        assert data == {
            "id": str(dataset_id),
            "catalog_record": {
                **data["catalog_record"],
                "organization": temp_org.dict(),
            },
            "title": "Other title",
            "description": "Other description",
            "service": "Other service",
            "geographical_coverage": "Hauts-de-France",
            "formats": [
                DataFormatView(id=1, name="Fichier tabulaire (XLS, XLSX, CSV, ...)")
            ],
            "technical_source": "Other information system",
            "producer_email": "other.service@mydomain.org",
            "contact_emails": ["other.person@mydomain.org"],
            "update_frequency": "weekly",
            "last_updated_at": other_last_updated_at.isoformat(),
            "url": "https://data.gouv.fr/datasets/other",
            "license": "ODC Open Database License",
            "tags": [],
            "extra_field_values": [],
            "headlines": None,
            "publication_restriction": PublicationRestriction.LEGAL_RESTRICTION.value,
        }

        # Entity was indeed updated
        query = GetDatasetByID(id=dataset_id, account=temp_user.account)
        dataset = await bus.execute(query)
        assert dataset.title == "Other title"
        assert dataset.description == "Other description"
        assert dataset.service == "Other service"
        assert dataset.geographical_coverage == "Hauts-de-France"
        assert dataset.formats == [
            DataFormatView(id=1, name="Fichier tabulaire (XLS, XLSX, CSV, ...)")
        ]
        assert dataset.technical_source == "Other information system"
        assert dataset.producer_email == "other.service@mydomain.org"
        assert dataset.contact_emails == ["other.person@mydomain.org"]
        assert dataset.update_frequency == UpdateFrequency.WEEKLY
        assert dataset.last_updated_at == other_last_updated_at
        assert dataset.url == "https://data.gouv.fr/datasets/other"
        assert dataset.license == "ODC Open Database License"

    async def test_can_not_update_publication_restriction_if_i_do_not_belong_to_the_organization(  # noqa: E501
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)

        siret = await bus.execute(CreateOrganizationFactory.build())

        user = await create_test_password_user(
            CreatePasswordUserFactory.build(organization_siret=siret)
        )

        dataset_id = await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account,
                organization_siret=temp_org.siret,
                publication_restriction=PublicationRestriction.NO_RESTRICTION,
            )
        )

        other_last_updated_at = fake.date_time_tz()

        payload = to_payload(
            UpdateDatasetPayloadFactory.build(
                title="Other title",
                description="Other description",
                service="Other service",
                geographical_coverage="Hauts-de-France",
                formats=["Base de données"],
                technical_source="Other information system",
                producer_email="other.service@mydomain.org",
                contact_emails=["other.person@mydomain.org"],
                update_frequency=UpdateFrequency.WEEKLY,
                last_updated_at=other_last_updated_at.isoformat(),
                url="https://data.gouv.fr/datasets/other",
                license="ODC Open Database License",
                tag_ids=[],
                extra_field_values=[],
                publication_restriction=PublicationRestriction.LEGAL_RESTRICTION.value,
            )
        )

        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=user.auth
        )
        assert response.status_code == 403


@pytest.mark.asyncio
class TestFormats:
    async def test_formats_add(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)
        command = CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            format_ids=[1],
        )
        dataset_id = await bus.execute(command)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json=to_payload(
                UpdateDatasetPayloadFactory.build_from_create_command(
                    command.copy(exclude={"format_ids"}),
                    format_ids=[1, 2],
                )
            ),
            auth=temp_user.auth,
        )

        assert response.status_code == 200
        assert response.json()["formats"] == [
            DataFormatView(id=1, name="Fichier tabulaire (XLS, XLSX, CSV, ...)"),
            DataFormatView(id=2, name="Fichier SIG (Shapefile, ...)"),
        ]

    async def test_formats_remove(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)
        command = CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            format_ids=[1, 2],
        )
        dataset_id = await bus.execute(command)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json=to_payload(
                UpdateDatasetPayloadFactory.build_from_create_command(
                    command.copy(exclude={"format_ids"}),
                    format_ids=[2],
                )
            ),
            auth=temp_user.auth,
        )

        assert response.status_code == 200
        assert response.json()["formats"] == [
            DataFormatView(id=2, name="Fichier SIG (Shapefile, ...)")
        ]


@pytest.mark.asyncio
class TestTags:
    async def test_tags_add(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)

        command = CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
        )
        dataset_id = await bus.execute(command)
        tag_architecture_id = await bus.execute(CreateTag(name="Architecture"))
        tag_architecture = await bus.execute(GetTagByID(id=tag_architecture_id))

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json=to_payload(
                UpdateDatasetPayloadFactory.build_from_create_command(
                    command.copy(exclude={"tag_ids"}),
                    tag_ids=[str(tag_architecture_id)],
                )
            ),
            auth=temp_user.auth,
        )
        assert response.status_code == 200
        assert response.json()["tags"] == [
            {"id": str(tag_architecture.id), "name": "Architecture"},
        ]

        dataset = await bus.execute(
            GetDatasetByID(id=dataset_id, account=temp_user.account)
        )
        assert dataset.tags == [tag_architecture]

    async def test_tags_remove(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)

        tag_architecture_id = await bus.execute(CreateTag(name="Architecture"))
        command = CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            tag_ids=[str(tag_architecture_id)],
        )
        dataset_id = await bus.execute(command)

        response = await client.put(
            f"/datasets/{dataset_id}/",
            json=to_payload(
                UpdateDatasetPayloadFactory.build_from_create_command(
                    command.copy(exclude={"tag_ids"}),
                    tag_ids=[],
                )
            ),
            auth=temp_user.auth,
        )
        assert response.status_code == 200
        assert response.json()["tags"] == []

        dataset = await bus.execute(
            GetDatasetByID(id=dataset_id, account=temp_user.account)
        )
        assert dataset.tags == []


@pytest.mark.asyncio
class TestExtraFieldValues:
    async def _setup(
        self,
    ) -> Tuple[Siret, TestPasswordUser, ID]:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())

        await bus.execute(
            CreateCatalog(
                organization_siret=siret,
                extra_fields=[
                    TextExtraField(
                        organization_siret=siret,
                        name="donnees_taille",
                        title="Taille du jeu de données",
                        hint_text="Informations sur la volumétrie du jeu de données",
                    )
                ],
            )
        )

        catalog = await bus.execute(GetCatalogBySiret(siret=siret))
        extra_field_id = catalog.extra_fields[0].id

        user = await create_test_password_user(
            CreatePasswordUserFactory.build(organization_siret=siret)
        )

        return siret, user, extra_field_id

    async def test_create_dataset_with_extra_field_values(
        self, client: httpx.AsyncClient
    ) -> None:
        siret, user, extra_field_id = await self._setup()

        payload = to_payload(
            CreateDatasetPayloadFactory.build(
                organization_siret=siret,
                extra_field_values=[
                    ExtraFieldValue(extra_field_id=extra_field_id, value="2.4 Go")
                ],
            )
        )
        response = await client.post("/datasets/", json=payload, auth=user.auth)
        assert response.status_code == 201
        data = response.json()
        assert data["extra_field_values"] == [
            {
                "extra_field_id": str(extra_field_id),
                "value": "2.4 Go",
            }
        ]

    async def test_add_extra_field_value(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        siret, user, extra_field_id = await self._setup()

        command = CreateDatasetFactory.build(
            account=user.account, organization_siret=siret
        )
        dataset_id = await bus.execute(command)
        dataset = await bus.execute(GetDatasetByID(id=dataset_id, account=user.account))
        assert not dataset.extra_field_values

        payload = to_payload(
            UpdateDatasetPayloadFactory.build_from_create_command(
                command.copy(exclude={"extra_field_values"}),
                extra_field_values=[
                    ExtraFieldValue(
                        extra_field_id=extra_field_id,
                        value="Environ 10 To",
                    )
                ],
            )
        )
        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=user.auth
        )
        assert response.status_code == 200
        data = response.json()
        assert data["extra_field_values"] == [
            {
                "extra_field_id": str(extra_field_id),
                "value": "Environ 10 To",
            }
        ]

    async def test_remove_extra_field_value(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        siret, user, extra_field_id = await self._setup()

        command = CreateDatasetFactory.build(
            account=user.account,
            organization_siret=siret,
            format_ids=[1, 2],
            extra_field_values=[
                ExtraFieldValue(
                    extra_field_id=extra_field_id,
                    value="2.4 Go",
                )
            ],
        )
        dataset_id = await bus.execute(command)
        dataset = await bus.execute(GetDatasetByID(id=dataset_id, account=user.account))
        assert len(dataset.extra_field_values) == 1

        payload = to_payload(
            UpdateDatasetPayloadFactory.build_from_create_command(
                command.copy(exclude={"extra_field_values"}),
                extra_field_values=[],
            )
        )
        response = await client.put(
            f"/datasets/{dataset_id}/", json=payload, auth=user.auth
        )
        assert response.status_code == 200
        data = response.json()
        assert data["extra_field_values"] == []

        # ExtraFieldValue row was indeed dropped from DB.
        database = resolve(Database)
        async with database.session() as session:
            stmt = select(ExtraFieldValueModel).where(
                ExtraFieldValueModel.dataset_id == dataset_id
            )
            result = await session.execute(stmt)
            assert not list(result.scalars())

    async def test_fetch_dataset_filtered_by_extra_field_value(
        self, client: httpx.AsyncClient
    ) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())

        extra_fields: List[ExtraField] = [
            TextExtraField(
                title="Latitude GPS du MTE",
                hint_text="La latitude où se trouve le MTE",
                name="latitude_mte",
                organization_siret=siret,
            ),
            BoolExtraField(
                data={
                    "false_value": "Oui",
                    "true_value": "Non",
                },
                title="Type de données",
                hint_text="Est-ce que ces données sont des données ?",
                name="type_donnees",
                organization_siret=siret,
            ),
        ]

        await bus.execute(
            CreateCatalog(organization_siret=siret, extra_fields=extra_fields)
        )

        catalog = await bus.execute(GetCatalogBySiret(siret=siret))

        user = await create_test_password_user(
            CreatePasswordUserFactory.build(organization_siret=siret)
        )

        value_1 = "48.891980000000046"
        value_2 = "Non"

        command = CreateDatasetFactory.build(
            account=user.account,
            organization_siret=siret,
            format_ids=[1, 2],
            extra_field_values=[
                ExtraFieldValue(
                    extra_field_id=catalog.extra_fields[0].id, value=value_1
                ),
                ExtraFieldValue(
                    extra_field_id=catalog.extra_fields[1].id, value=value_2
                ),
            ],
        )

        await bus.execute(command)

        command = CreateDatasetFactory.build(
            account=user.account,
            organization_siret=siret,
            format_ids=[1, 2],
            extra_field_values=[
                ExtraFieldValue(
                    extra_field_id=catalog.extra_fields[0].id, value="85Go"
                ),
                ExtraFieldValue(extra_field_id=catalog.extra_fields[1].id, value="Oui"),
            ],
        )

        await bus.execute(command)

        command = CreateDatasetFactory.build(
            title="Tata",
            account=user.account,
            organization_siret=siret,
            format_ids=[1, 2],
        )

        await bus.execute(command)

        params = {
            "extra_field_values": json.dumps(
                [
                    {
                        "extra_field_id": str(
                            catalog.extra_fields[0].id,
                        ),
                        "value": value_1,
                    },
                    {
                        "extra_field_id": str(
                            catalog.extra_fields[1].id,
                        ),
                        "value": value_2,
                    },
                ]
            )
        }

        response = await client.get("/datasets/", params=params, auth=user.auth)

        assert response.status_code == 200

        data = response.json()

        assert data["total_items"] == 1


@pytest.mark.asyncio
class TestDeleteDataset:
    async def test_delete(
        self,
        client: httpx.AsyncClient,
        temp_org: OrganizationView,
        temp_user: TestPasswordUser,
        admin_user: TestPasswordUser,
    ) -> None:
        bus = resolve(MessageBus)

        dataset_id = await bus.execute(
            CreateDatasetFactory.build(
                account=temp_user.account, organization_siret=temp_org.siret
            )
        )

        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204

        with pytest.raises(DatasetDoesNotExist):
            await bus.execute(GetDatasetByID(id=dataset_id, account=temp_user.account))

    async def test_idempotent(
        self, client: httpx.AsyncClient, admin_user: TestPasswordUser
    ) -> None:
        # Repeated calls on a deleted (or non-existing) resource should be fine.
        dataset_id = id_factory()
        response = await client.delete(f"/datasets/{dataset_id}/", auth=admin_user.auth)
        assert response.status_code == 204
