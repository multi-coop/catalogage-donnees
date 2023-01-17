import httpx
import pytest

from ..helpers import TestPasswordUser


@pytest.mark.asyncio
async def test_dataformat_list(
    client: httpx.AsyncClient, temp_user: TestPasswordUser
) -> None:

    response = await client.get("/dataformat/", auth=temp_user.auth)
    assert response.status_code == 200

    data = response.json()
    assert sorted(data, key=lambda x: x["id"], reverse=False) == [
        {"id": 1, "name": "Fichier tabulaire (XLS, XLSX, CSV, ...)"},
        {"id": 2, "name": "Fichier SIG (Shapefile, ...)"},
        {"id": 3, "name": "API (REST, GraphQL, ...)"},
        {"id": 4, "name": "Base de données"},
        {"id": 5, "name": "Site web"},
        {"id": 6, "name": "Autre"},
    ]


@pytest.mark.asyncio
class TestTagsPermissions:
    async def test_dataformat_list_not_authenticated(
        self, client: httpx.AsyncClient
    ) -> None:
        response = await client.get("/dataformat/")
        assert response.status_code == 401