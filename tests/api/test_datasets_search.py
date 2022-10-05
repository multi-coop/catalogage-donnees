import random
from typing import List, Optional, Tuple

import httpx
import pytest

from server.application.datasets.commands import DeleteDataset
from server.application.datasets.queries import GetDatasetByID
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateDatasetFactory, UpdateDatasetFactory

from ..helpers import TestPasswordUser

DEFAULT_CORPUS_ITEMS = [
    ("Inventaire national forestier", "Ensemble des forêts de France"),
    ("Base Carbone", "Inventaire des données climat de l'ADEME"),
    ("Cadastre national", "Base de données du cadastre de la France"),
]


async def add_test_datasets(
    organization: OrganizationView,
    user: TestPasswordUser,
    *,
    items: List[Tuple[str, str]] = None
) -> None:
    if items is None:
        items = DEFAULT_CORPUS_ITEMS

    bus = resolve(MessageBus)

    for title, description in items:
        command = CreateDatasetFactory.build(
            account=user.account,
            organization_siret=organization.siret,
            title=title,
            description=description,
        )
        pk = await bus.execute(command)
        query = GetDatasetByID(id=pk)
        await bus.execute(query)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, expected_titles",
    [
        pytest.param(
            "",
            [],
            id="terms:none",
        ),
        pytest.param(
            "hello!? hm?m & || specia| ch@rs'); \"quote",
            [],
            id="terms:garbage",
        ),
        pytest.param(
            "tototitu",
            [],
            id="terms:single-results:none",
        ),
        pytest.param(
            "carbone",
            ["Base Carbone"],
            id="terms:single-result:single-title",
        ),
        pytest.param(
            "forêt",
            ["Inventaire national forestier"],
            id="terms:single-result:single-description",
        ),
        pytest.param(
            "national",
            ["Cadastre national", "Inventaire national forestier"],
            id="terms:single-results:multiple-title",
        ),
        pytest.param(
            "France",
            ["Cadastre national", "Inventaire national forestier"],
            id="terms:single-results:multiple-description",
        ),
        pytest.param(
            "base",
            ["Cadastre national", "Base Carbone"],
            id="terms:single-results:multiple-title-description",
        ),
        pytest.param(
            "données cadastre",
            ["Cadastre national"],
            id="terms:multiple-results:single",
        ),
    ],
)
async def test_search(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    q: str,
    expected_titles: List[str],
) -> None:
    await add_test_datasets(temp_org, temp_user)

    response = await client.get(
        "/datasets/",
        params={"q": q},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data["items"]]
    assert titles == expected_titles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q_ref, q_other",
    [
        pytest.param(
            "forêt",
            "forestier",
            id="lexemes",
        ),
        pytest.param(
            "base",
            "BaSe",
            id="case-insensitive",
        ),
    ],
)
async def test_search_robustness(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    q_ref: str,
    q_other: str,
) -> None:
    await add_test_datasets(temp_org, temp_user)

    response = await client.get(
        "/datasets/",
        params={"q": q_ref},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    reference_titles = [item["title"] for item in data["items"]]
    assert reference_titles

    response = await client.get(
        "/datasets/",
        params={"q": q_other},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    other_titles = [item["title"] for item in data["items"]]

    assert reference_titles == other_titles


@pytest.mark.asyncio
async def test_search_results_change_when_data_changes(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
) -> None:
    await add_test_datasets(temp_org, temp_user)

    bus = resolve(MessageBus)

    # No results initially
    response = await client.get(
        "/datasets/",
        params={"q": "titre"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert not data["items"]

    # Add new dataset
    command = CreateDatasetFactory.build(
        account=temp_user.account, organization_siret=temp_org.siret, title="Titre"
    )
    pk = await bus.execute(command)
    # New dataset is returned in search results
    response = await client.get(
        "/datasets/",
        params={"q": "titre"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()["items"]
    assert dataset["id"] == str(pk)

    # Update dataset title
    update_command = UpdateDatasetFactory.build(
        account=temp_user.account,
        id=pk,
        title="Modifié",
        **command.dict(exclude={"title", "account", "organization_siret"}),
    )

    await bus.execute(update_command)
    # Updated dataset is returned in search results targeting updated data
    response = await client.get(
        "/datasets/",
        params={"q": "modifié"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()["items"]
    assert dataset["id"] == str(pk)

    # Same on description
    update_command = UpdateDatasetFactory.build(
        description="Jeu de données spécial",
        **update_command.dict(exclude={"description"}),
    )
    await bus.execute(update_command)
    response = await client.get(
        "/datasets/",
        params={"q": "spécial"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    (dataset,) = response.json()["items"]
    assert dataset["id"] == str(pk)

    # Deleted dataset is not returned in search results anymore
    delete_command = DeleteDataset(id=pk)
    await bus.execute(delete_command)
    response = await client.get(
        "/datasets/",
        params={"q": "modifié"},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert not data["items"]


@pytest.mark.asyncio
async def test_search_ranking(
    client: httpx.AsyncClient, temp_org: OrganizationView, temp_user: TestPasswordUser
) -> None:
    items = [
        ("A", "..."),
        ("B", "Forêt nouvelle"),
        ("C", "Historique des forêts anciennes"),
        ("D", "Ancien historique des forêts"),
    ]

    random.shuffle(items)  # Ensure DB insert order is irrelevant.

    await add_test_datasets(temp_org, temp_user, items=items)

    q = "Forêt ancienne"  # Lexemes: forêt, ancien

    expected_titles = [
        "C",  # Both lexemes match, close to each other
        "D",  # Both lexemes match, further away from each other
    ]

    response = await client.get("/datasets/", params={"q": q}, auth=temp_user.auth)
    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data["items"]]
    assert titles == expected_titles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "corpus, q, expected_headlines",
    [
        pytest.param(
            [("Restaurants CROUS", "Lieux de restauration du CROUS")],
            "restaurant",
            {
                "title": "<mark>Restaurants</mark> CROUS",
                "description": "Lieux de <mark>restauration</mark> du CROUS",
            },
            id="title-description",
        ),
        pytest.param(
            [("Restaurants CROUS", "Données fournies par le CROUS")],
            "restaurant",
            {
                "title": "<mark>Restaurants</mark> CROUS",
                "description": None,
            },
            id="description-without-results",
        ),
    ],
)
async def test_search_highlight(
    client: httpx.AsyncClient,
    temp_org: OrganizationView,
    temp_user: TestPasswordUser,
    corpus: list,
    q: str,
    expected_headlines: Optional[dict],
) -> None:
    await add_test_datasets(temp_org, temp_user, items=corpus)

    q = "restaurant"

    response = await client.get(
        "/datasets/",
        params={"q": q},
        auth=temp_user.auth,
    )
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1

    assert items[0]["headlines"] == expected_headlines
