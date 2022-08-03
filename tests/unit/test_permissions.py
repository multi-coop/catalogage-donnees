from typing import Any

import httpx
import pytest
from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKeyHeader
from fastapi.security.http import HTTPBearer

from server.api.auth.backends.token import TokenAuthBackend
from server.api.auth.middleware import AuthMiddleware
from server.api.auth.permissions import (
    BasePermission,
    HasAPIKey,
    HasRole,
    IsAuthenticated,
)
from server.api.types import APIRequest
from server.domain.auth.entities import UserRole

from ..helpers import TestPasswordUser


@pytest.mark.asyncio
async def test_is_authenticated(temp_user: TestPasswordUser) -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get("/", dependencies=[Depends(IsAuthenticated())])
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.account.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_has_role(
    temp_user: TestPasswordUser, admin_user: TestPasswordUser
) -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get("/", dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))])
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 401

        headers = {"Authorization": f"Bearer {temp_user.account.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 403

        headers = {"Authorization": f"Bearer {admin_user.account.api_token}"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_has_role_requires_is_authenticated() -> None:
    app = FastAPI()

    app.add_middleware(AuthMiddleware, backend=TokenAuthBackend())

    @app.get(
        "/",
        dependencies=[
            # Should be: 'Depends(IsAuthenticated() & HasRole(...))'
            Depends(HasRole(UserRole.ADMIN)),
        ],
    )
    async def index() -> str:
        return "OK"  # pragma: no cover

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        with pytest.raises(RuntimeError, match="IsAuthenticated"):
            await client.get("/")


@pytest.mark.asyncio
async def test_bitwise_or() -> None:
    class HasHeader(BasePermission):
        def __init__(self, name: str) -> None:
            self._name = name

        def has_permission(self, request: APIRequest) -> bool:
            return self._name in request.headers

    with pytest.raises(NotImplementedError):
        HasHeader("X-Header") | "not a permission"

    app = FastAPI()

    @app.get(
        "/", dependencies=[Depends(HasHeader("X-HeaderA") | HasHeader("X-HeaderB"))]
    )
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 403

        response = await client.get("/", headers={"X-HeaderA": "true"})
        assert response.status_code == 200

        response = await client.get("/", headers={"X-HeaderB": "true"})
        assert response.status_code == 200

        response = await client.get(
            "/", headers={"X-HeaderA": "true", "X-HeaderB": "true"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_bitwise_and() -> None:
    class HasHeader(BasePermission):
        def __init__(self, name: str) -> None:
            self._name = name

        def has_permission(self, request: APIRequest) -> bool:
            return self._name in request.headers

    with pytest.raises(NotImplementedError):
        HasHeader("X-Header") & "not a permission"

    app = FastAPI()

    @app.get(
        "/", dependencies=[Depends(HasHeader("X-HeaderA") & HasHeader("X-HeaderB"))]
    )
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 403

        response = await client.get("/", headers={"X-HeaderA": "true"})
        assert response.status_code == 403

        response = await client.get("/", headers={"X-HeaderB": "true"})
        assert response.status_code == 403

        response = await client.get(
            "/", headers={"X-HeaderA": "true", "X-HeaderB": "true"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_bitwise_openapi_security_schemes() -> None:
    class PermA(BasePermission):
        def __call__(
            self,
            request: APIRequest,
            _: str = Depends(APIKeyHeader(name="Api-Key", scheme_name="API Key")),
        ) -> None:
            ...  # pragma: no cover

    class PermB(BasePermission):
        def __call__(
            self,
            request: APIRequest,
            other_dependency: str = Depends(lambda: "Some value"),
            _: Any = Depends(HTTPBearer(scheme_name="Bearer")),
        ) -> None:
            ...  # pragma: no cover

    app = FastAPI()

    @app.post("/users/", dependencies=[Depends(PermA() | PermB())])
    async def create_user() -> str:
        return "OK"  # pragma: no cover

    @app.delete("/users/", dependencies=[Depends(PermA() & PermB())])
    async def delete_user() -> str:
        return "OK"  # pragma: no cover

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()

        assert "API Key" in schema["components"]["securitySchemes"]
        assert "Bearer" in schema["components"]["securitySchemes"]

        # OR
        assert {"API Key": []} in schema["paths"]["/users/"]["post"]["security"]
        assert {"Bearer": []} in schema["paths"]["/users/"]["post"]["security"]

        # AND
        assert {"API Key": []} in schema["paths"]["/users/"]["delete"]["security"]
        assert {"Bearer": []} in schema["paths"]["/users/"]["delete"]["security"]


@pytest.mark.asyncio
async def test_has_api_key() -> None:
    app = FastAPI()

    @app.get("/", dependencies=[Depends(HasAPIKey())])
    async def index() -> str:
        return "OK"

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 403

        headers = {"X-Api-Key": "<testing>"}
        response = await client.get("/", headers=headers)
        assert response.status_code == 200
