import httpx
import pytest

from server.application.tags.commands import CreateTag
from server.config.di import resolve
from server.seedwork.application.messages import MessageBus

from ..helpers import TestPasswordUser


@pytest.mark.asyncio
async def test_tags_list(
    client: httpx.AsyncClient, temp_user: TestPasswordUser
) -> None:
    bus = resolve(MessageBus)

    response = await client.get("/tags/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == []

    id_services = await bus.execute(CreateTag(name="services"))
    id_architecture = await bus.execute(CreateTag(name="architecture"))

    response = await client.get("/tags/", auth=temp_user.auth)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(id_architecture),
            "name": "architecture",
        },
        {
            "id": str(id_services),
            "name": "services",
        },
    ]


@pytest.mark.asyncio
class TestTagsPermissions:
    async def test_tags_list_not_authenticated(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/tags/")
        assert response.status_code == 401
