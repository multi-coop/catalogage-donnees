import json
from typing import Callable

import httpx
from pydantic import BaseModel

from server.config.di import resolve
from server.domain.auth.entities import PasswordUser, UserRole
from server.domain.auth.repositories import PasswordUserRepository
from server.seedwork.application.messages import MessageBus

from .factories import CreatePasswordUserFactory


def create_client(app: Callable) -> httpx.AsyncClient:
    return httpx.AsyncClient(app=app, base_url="http://testserver")


def to_payload(obj: BaseModel) -> dict:
    """
    Convert a Pydantic model instance to a JSON-serializable dictionary.
    """
    return json.loads(obj.json())


class TestPasswordUser(PasswordUser):
    """
    A user that exposes the plaintext password for testing purposes.
    """

    __test__ = False  # pytest shouldn't collect this.

    password: str

    def auth(self, request: httpx.Request) -> httpx.Request:
        """An auth function for use with HTTPX.

        Usage:
            response = client.post(..., auth=test_user.auth)
        """
        request.headers["Authorization"] = f"Bearer {self.account.api_token}"
        return request


async def create_test_password_user(role: UserRole) -> TestPasswordUser:
    bus = resolve(MessageBus)
    password_user_repository = resolve(PasswordUserRepository)

    command = CreatePasswordUserFactory.build()
    await bus.execute(command, role=role)

    user = await password_user_repository.get_by_email(command.email)
    assert user is not None

    return TestPasswordUser(**user.dict(), password=command.password.get_secret_value())


def api_key_auth(request: httpx.Request) -> httpx.Request:
    request.headers["X-Api-Key"] = "<testing>"
    return request
