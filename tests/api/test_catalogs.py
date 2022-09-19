from typing import List

import httpx
import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret
from server.application.datasets.queries import GetDatasetByID
from server.config.di import resolve
from server.domain.catalogs.entities import ExtraFieldType, TextExtraField
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus

from ..factories import CreateDatasetFactory, CreateOrganizationFactory, fake
from ..helpers import TestPasswordUser, api_key_auth


@pytest.mark.asyncio
async def test_catalog_create(client: httpx.AsyncClient) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build(name="Org 1"))

    response = await client.post(
        "/catalogs/", json={"organization_siret": str(siret)}, auth=api_key_auth
    )
    assert response.status_code == 201
    assert response.json() == {
        "organization": {
            "siret": str(siret),
            "name": "Org 1",
        },
        "extra_fields": [],
    }
    catalog = await bus.execute(GetCatalogBySiret(siret=siret))
    assert catalog.organization.siret == siret

    dataset_id = await bus.execute(CreateDatasetFactory.build(organization_siret=siret))
    dataset = await bus.execute(GetDatasetByID(id=dataset_id))
    assert dataset.catalog_record.organization.siret == siret


@pytest.mark.asyncio
async def test_catalog_create_already_exists(client: httpx.AsyncClient) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build(name="Org 1"))
    await bus.execute(CreateCatalog(organization_siret=siret))

    response = await client.post(
        "/catalogs/", json={"organization_siret": str(siret)}, auth=api_key_auth
    )
    assert response.status_code == 200
    assert response.json() == {
        "organization": {
            "siret": str(siret),
            "name": "Org 1",
        },
        "extra_fields": [],
    }


@pytest.mark.asyncio
async def test_catalog_invalid_org_does_not_exist(client: httpx.AsyncClient) -> None:
    siret = Siret(fake.siret())
    response = await client.post(
        "/catalogs/", json={"organization_siret": str(siret)}, auth=api_key_auth
    )
    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extra_field, expected_errors_attrs",
    [
        pytest.param(
            {},
            [
                {
                    "loc": ["body", "extra_fields", 0, "name"],
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "extra_fields", 0, "title"],
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "extra_fields", 0, "hint_text"],
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "extra_fields", 0, "type"],
                    "type": "value_error.missing",
                },
            ],
            id="missing-fields",
        ),
        pytest.param(
            {
                "name": "donnees_taille",
                "title": "Taille du jeu de données",
                "hint_text": (
                    "Information sur la volumétrie et l'unité de mesure "
                    "associées au jeu de données."
                ),
                "type": "UNKNOWN_TYPE",
            },
            [
                {"loc": ["body", "extra_fields", 0], "type": "value_error"},
            ],
            id="invalid-type",
        ),
        pytest.param(
            {
                "name": "donnees_taille",
                "title": "Taille du jeu de données",
                "hint_text": (
                    "Information sur la volumétrie et l'unité de mesure "
                    "associées au jeu de données."
                ),
                "type": "ENUM",
                "data": {"not_values": "blah"},
            },
            [
                {
                    "loc": [
                        "body",
                        "extra_fields",
                        "__root__",
                        0,
                        "EnumExtraField",
                        "data",
                        "values",
                    ],
                    "type": "value_error.missing",
                },
            ],
            id="invalid-enum-data",
        ),
        pytest.param(
            {
                "name": "donnees_taille",
                "title": "Taille du jeu de données",
                "hint_text": (
                    "Information sur la volumétrie et l'unité de mesure "
                    "associées au jeu de données."
                ),
                "type": "BOOL",
                "data": {"true_value": "Oui", "typo_false_value": "Non"},
            },
            [
                {
                    "loc": [
                        "body",
                        "extra_fields",
                        "__root__",
                        0,
                        "BoolExtraField",
                        "data",
                        "false_value",
                    ],
                    "type": "value_error.missing",
                },
            ],
            id="invalid-bool-data",
        ),
    ],
)
async def test_create_catalog_invalid_extra_fields(
    client: httpx.AsyncClient, extra_field: dict, expected_errors_attrs: list
) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build())

    response = await client.post(
        "/catalogs/",
        json={"organization_siret": str(siret), "extra_fields": [extra_field]},
        auth=api_key_auth,
    )
    assert response.status_code == 422
    data = response.json()

    assert len(data["detail"]) == len(expected_errors_attrs)

    for error, expected_error_attrs in zip(data["detail"], expected_errors_attrs):
        error_attrs = {key: error[key] for key in expected_error_attrs}
        assert error_attrs == expected_error_attrs


@pytest.mark.asyncio
async def test_create_catalog_with_extra_fields(client: httpx.AsyncClient) -> None:
    bus = resolve(MessageBus)
    siret = await bus.execute(CreateOrganizationFactory.build(name="Org 1"))

    extra_fields: List[dict] = [
        {
            "name": "donnees_taille",
            "title": "Taille du jeu de données",
            "hint_text": (
                "Information sur la volumétrie et l'unité de mesure "
                "associées au jeu de données."
            ),
            "type": "TEXT",
        },
        {
            "name": "domaine",
            "title": "Domaine",
            "hint_text": "Nom du domaine associé au jeu de données.",
            "type": "ENUM",
            "data": {
                "values": [
                    "Audiovisuel",
                    "Patrimoine",
                    "Archives",
                ]
            },
        },
        {
            "name": "donnees_perso",
            "title": "Données à caractère personnel",
            "hint_text": (
                "Ce jeu de données contient-il des données à caractère " "personnel ?"
            ),
            "type": "BOOL",
            "data": {"true_value": "Oui", "false_value": "Non"},
        },
    ]

    response = await client.post(
        "/catalogs/",
        json={"organization_siret": str(siret), "extra_fields": extra_fields},
        auth=api_key_auth,
    )
    assert response.status_code == 201
    data = response.json()

    assert data == {
        "organization": {
            "siret": str(siret),
            "name": "Org 1",
        },
        "extra_fields": [
            {
                "id": data["extra_fields"][0]["id"],
                "name": "donnees_taille",
                "title": "Taille du jeu de données",
                "hint_text": (
                    "Information sur la volumétrie et l'unité de mesure "
                    "associées au jeu de données."
                ),
                "type": "TEXT",
                "data": {},
            },
            {
                "id": data["extra_fields"][1]["id"],
                "name": "domaine",
                "title": "Domaine",
                "hint_text": "Nom du domaine associé au jeu de données.",
                "type": "ENUM",
                "data": {
                    "values": [
                        "Audiovisuel",
                        "Patrimoine",
                        "Archives",
                    ]
                },
            },
            {
                "id": data["extra_fields"][2]["id"],
                "name": "donnees_perso",
                "title": "Données à caractère personnel",
                "hint_text": (
                    "Ce jeu de données contient-il des données à caractère "
                    "personnel ?"
                ),
                "type": "BOOL",
                "data": {"true_value": "Oui", "false_value": "Non"},
            },
        ],
    }

    # Check catalog exists with expected extra fields.
    catalog = await bus.execute(GetCatalogBySiret(siret=siret))
    assert len(catalog.extra_fields) == 3
    field0, field1, field2 = catalog.extra_fields
    assert field0.name == "donnees_taille"
    assert field1.name == "domaine"
    # Make extensive checks on one of the fields.
    assert field2.name == "donnees_perso"
    assert field2.title == "Données à caractère personnel"
    assert (
        field2.hint_text
        == "Ce jeu de données contient-il des données à caractère personnel ?"
    )
    assert field2.type == ExtraFieldType.BOOL
    assert field2.data == {"true_value": "Oui", "false_value": "Non"}


@pytest.mark.asyncio
async def test_get_catalog(
    client: httpx.AsyncClient, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    siret = await bus.execute(CreateOrganizationFactory.build(name="Org 1"))
    response = await client.get(f"/catalogs/{siret}/", auth=temp_user.auth)
    assert response.status_code == 404

    await bus.execute(
        CreateCatalog(
            organization_siret=siret,
            extra_fields=[
                TextExtraField(
                    organization_siret=siret,
                    name="domaine",
                    title="Domaine",
                    hint_text="Domaine associé au jeu de données",
                )
            ],
        )
    )
    response = await client.get(f"/catalogs/{siret}/", auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "organization": {
            "siret": siret,
            "name": "Org 1",
        },
        "extra_fields": [
            {
                "id": data["extra_fields"][0]["id"],
                "type": "TEXT",
                "name": "domaine",
                "title": "Domaine",
                "hint_text": "Domaine associé au jeu de données",
                "data": {},
            }
        ],
    }


@pytest.mark.asyncio
class TestCatalogPermissions:
    async def test_create_anonymous_forbidden(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())
        response = await client.post(
            "/catalogs/", json={"organization_siret": str(siret)}
        )
        assert response.status_code == 403

    async def test_create_authenticated_forbidden(
        self, client: httpx.AsyncClient, temp_user: TestPasswordUser
    ) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())
        response = await client.post(
            "/catalogs/", json={"organization_siret": str(siret)}, auth=temp_user.auth
        )
        assert response.status_code == 403

    async def test_get_not_authenticated(self, client: httpx.AsyncClient) -> None:
        bus = resolve(MessageBus)
        siret = await bus.execute(CreateOrganizationFactory.build())
        await bus.execute(CreateCatalog(organization_siret=siret))
        response = await client.get(f"/catalogs/{siret}/")
        assert response.status_code == 401
