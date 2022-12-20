from dataclasses import dataclass
from typing import Callable

import httpx
import pytest

from server.application.catalogs.commands import CreateCatalog
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.domain.common.types import ID, id_factory
from server.domain.datasets.entities import DataFormat
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus

from ..factories import (
    CreateDatasetFactory,
    CreateOrganizationFactory,
    CreatePasswordUserFactory,
    CreateTagFactory,
)
from ..helpers import TestPasswordUser, create_test_password_user


@pytest.mark.asyncio
async def test_dataset_filters_info(
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    organization_logo_url = (
        "https://upload.wikimedia.org/wikipedia/commons/6/60/Edward_Snowden-2.jpg"
    )

    siret_non_empty = await bus.execute(
        CreateOrganizationFactory.build(
            name="A - Organization with a non-empty catalog",
            logo_url=organization_logo_url,
        )
    )
    await bus.execute(CreateCatalog(organization_siret=siret_non_empty))

    siret_empty = await bus.execute(
        CreateOrganizationFactory.build(
            name="B - Organization with an empty catalog",
            logo_url=organization_logo_url,
        )
    )
    await bus.execute(CreateCatalog(organization_siret=siret_empty))

    await bus.execute(
        CreateOrganizationFactory.build(
            name="C - Organization without a catalog", logo_url=organization_logo_url
        )
    )

    user = await create_test_password_user(
        CreatePasswordUserFactory.build(organization_siret=siret_non_empty)
    )

    tag_id = await bus.execute(CreateTagFactory.build(name="Architecture"))

    await bus.execute(
        CreateDatasetFactory.build(
            organization_siret=siret_non_empty,
            account=user.account,
            geographical_coverage="France métropolitaine",
            service="Same example service",
            technical_source="Example database system",
            license="Une licence spéciale",
        )
    )

    # Add another with filterable optional fields left out
    await bus.execute(
        CreateDatasetFactory.build(
            organization_siret=siret_non_empty,
            account=user.account,
            geographical_coverage="Région Nouvelle-Aquitaine",
            service="Same example service",
            technical_source=None,
        )
    )

    response = await client.get("/datasets/filters/", auth=temp_user.auth)
    assert response.status_code == 200

    data = response.json()

    assert set(data) == {
        "organization_siret",
        "geographical_coverage",
        "service",
        "format",
        "technical_source",
        "tag_id",
        "license",
    }

    assert data["organization_siret"] == [
        temp_org.dict(),
        {
            "siret": str(siret_non_empty),
            "name": "A - Organization with a non-empty catalog",
            "logo_url": organization_logo_url,
        },
        {
            "siret": str(siret_empty),
            "name": "B - Organization with an empty catalog",
            "logo_url": organization_logo_url,
        },
    ]

    assert data["geographical_coverage"] == [
        "France métropolitaine",
        "Région Nouvelle-Aquitaine",
    ]

    assert data["service"] == [
        "Same example service",
    ]

    assert sorted(data["format"]) == [
        "api",
        "database",
        "file_gis",
        "file_tabular",
        "other",
        "website",
    ]

    assert data["technical_source"] == [
        "Example database system",
    ]

    assert data["tag_id"] == [
        {"id": str(tag_id), "name": "Architecture"},
    ]

    assert data["license"] == [
        "*",
        "Licence Ouverte",
        "ODC Open Database License",
        "Une licence spéciale",
    ]


@dataclass
class _Env:
    siret_any: Siret
    siret_match: Siret
    tag_id: ID


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filtername, create_kwargs, negative_value, positive_value",
    [
        pytest.param(
            "organization_siret",
            lambda env: {"organization_siret": env.siret_match},
            lambda env: [str(env.siret_any)],
            lambda env: [str(env.siret_match)],
            id="organization_siret",
        ),
        pytest.param(
            "geographical_coverage",
            lambda _: {"geographical_coverage": "France métropolitaine"},
            lambda _: ["Hauts-de-France"],
            lambda _: ["France métropolitaine"],
            id="geographical_coverage",
        ),
        pytest.param(
            "service",
            lambda _: {"service": "Service cartes"},
            lambda _: ["Autre direction"],
            lambda _: ["Service cartes"],
            id="service",
        ),
        pytest.param(
            "format",
            lambda _: {"formats": [DataFormat.FILE_GIS.value]},
            lambda _: [DataFormat.DATABASE.value],
            lambda _: [DataFormat.FILE_GIS.value],
            id="format",
        ),
        pytest.param(
            "technical_source",
            lambda _: {"technical_source": "SGBD central"},
            lambda _: ["Autre système"],
            lambda _: ["SGBD central"],
            id="technical_source",
        ),
        pytest.param(
            "tag_id",
            lambda env: {"tag_ids": [env.tag_id]},
            lambda _: [str(id_factory())],
            lambda env: [str(env.tag_id)],
            id="tag_id",
        ),
        pytest.param(
            "license",
            lambda _: {"license": "Licence Ouverte"},
            lambda _: ["ODC Open License v1.0"],
            lambda _: "Licence Ouverte",
            id="license",
        ),
    ],
)
async def test_dataset_filters_apply(
    client: httpx.AsyncClient,
    temp_user: TestPasswordUser,
    filtername: str,
    create_kwargs: Callable[[_Env], dict],
    positive_value: Callable[[_Env], list],
    negative_value: Callable[[_Env], list],
) -> None:
    bus = resolve(MessageBus)

    siret_any = await bus.execute(CreateOrganizationFactory.build())
    await bus.execute(CreateCatalog(organization_siret=siret_any))

    siret_match = await bus.execute(CreateOrganizationFactory.build())
    await bus.execute(CreateCatalog(organization_siret=siret_match))

    tag_id = await bus.execute(CreateTagFactory.build())

    env = _Env(tag_id=tag_id, siret_any=siret_any, siret_match=siret_match)

    kwargs: dict = {"organization_siret": siret_any}
    kwargs.update(create_kwargs(env))

    user = await create_test_password_user(
        CreatePasswordUserFactory.build(organization_siret=kwargs["organization_siret"])
    )

    dataset_id = await bus.execute(
        CreateDatasetFactory.build(account=user.account, **kwargs)
    )

    params = {filtername: negative_value(env)}
    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0

    params = {filtername: positive_value(env)}
    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(dataset_id)


@pytest.mark.asyncio
async def test_dataset_filters_license_any(
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    dataset1_id = await bus.execute(
        CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            license="Licence Ouverte",
        )
    )
    dataset2_id = await bus.execute(
        CreateDatasetFactory.build(
            account=temp_user.account,
            organization_siret=temp_org.siret,
            license="ODC Open Database Licence v1.0",
        )
    )

    params = {"license": "*"}
    response = await client.get("/datasets/", params=params, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert [item["id"] for item in data["items"]] == [
        str(dataset2_id),
        str(dataset1_id),
    ]
