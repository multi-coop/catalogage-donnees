import json
from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
import pytest
from starlette.requests import Request

import server.config.di
from server.config.di import configure, resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.repositories import AccountRepository, DataPassUserRepository
from server.infrastructure.auth.datapass import DataPassOpenIDClient, DataPassUserInfo
from server.infrastructure.database import Database
from server.seedwork.application.di import Container
from server.seedwork.application.messages import MessageBus

from ..factories import (
    CreateDataPassUserFactory,
    CreateOrganizationFactory,
    CreatePasswordUserFactory,
)
from ..helpers import to_payload


@pytest.mark.asyncio
async def test_login(client: httpx.AsyncClient) -> None:
    response = await client.get("/auth/datapass/login/")
    assert response.status_code == 302
    redirect_url = httpx.URL(response.headers["Location"])

    # Verify the destination of the authentication request.
    assert redirect_url.scheme == "https"
    assert redirect_url.netloc == b"auth-staging.api.gouv.fr"
    assert redirect_url.path == "/oauth/authorize"

    # Verify the REQUIRED parameters for the OpenID Connect 'Authorization Code'
    # authentication request.
    # See: https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
    assert redirect_url.params["scope"] == "openid email organizations"
    assert redirect_url.params["response_type"] == "code"
    assert redirect_url.params["client_id"] == "<testing>"
    assert (
        redirect_url.params["redirect_uri"]
        == "http://testserver/auth/datapass/callback/"
    )


@pytest.mark.asyncio
class TestCallback:
    @asynccontextmanager
    async def _mock_openid_client(
        self,
        monkeypatch: pytest.MonkeyPatch,
        userinfo: DataPassUserInfo,
    ) -> AsyncIterator[None]:
        class MockDataPassOpenIDClient(DataPassOpenIDClient):
            async def authorize_userinfo(self, request: Request) -> DataPassUserInfo:
                # Skip validation of the request which the default Authlib client
                # would do, we only test our processing of the received "userinfo".
                return userinfo

        def configure_with_overrides(container: Container) -> None:
            configure(container)
            container.register_instance(
                DataPassOpenIDClient, MockDataPassOpenIDClient()
            )

        container = Container(configure_with_overrides)
        container.bootstrap()

        monkeypatch.setattr(server.config.di, "_CONTAINER", container)

        db = resolve(Database)
        async with db.autorollback():
            yield

    async def test_if_org_does_not_exist_yet_then_redirects_to_org_creation_help_page(
        self, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        userinfo: DataPassUserInfo = {
            "email": "johndoe@mydomain.org",
            "organizations": [
                {
                    "siret": "11122233344441",
                    "label": "Some organization",
                },
            ],
        }

        async with self._mock_openid_client(monkeypatch, userinfo):
            response = await client.get("/auth/datapass/callback/")
            assert response.status_code == 307
            assert (
                response.headers["Location"]
                == "http://client.testserver/auth/datapass/create-organization"
            )

    async def test_if_more_than_one_org_exists_then_redirects_to_org_picker(
        self, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bus = resolve(MessageBus)

        email = "johndoe@mydomain.org"
        siret_1 = "11122233344441"
        siret_2 = "11122233344442"

        userinfo: DataPassUserInfo = {
            "email": email,
            "organizations": [
                {
                    "siret": siret_1,
                    "label": "Organization 1",
                },
                {"siret": siret_2, "label": "Organization 2"},
                {"siret": "11122233344443", "label": "Other organization"},
            ],
        }

        async with self._mock_openid_client(monkeypatch, userinfo):
            await bus.execute(CreateOrganizationFactory.build(siret=siret_1))
            await bus.execute(CreateOrganizationFactory.build(siret=siret_2))

            response = await client.get("/auth/datapass/callback/")
            assert response.status_code == 307
            location = httpx.URL(response.headers["Location"])
            assert location.scheme == "http"
            assert location.netloc == b"client.testserver"
            assert location.path == "/auth/datapass/pick-organization"
            info = json.loads(location.params["info"])
            assert info == {
                "email": email,
                "organizations": [
                    {"siret": siret_1, "name": "Organization 1"},
                    {"siret": siret_2, "name": "Organization 2"},
                ],
            }

            # Backend provides an opaque token.
            token = location.params["token"]

            # Frontend may then use this token to register the user in the chosen org.

            # Without this token, request is not authorized...
            payload = to_payload(
                CreateDataPassUserFactory.build(organization_siret=siret_1, email=email)
            )
            response = await client.post("/auth/datapass/users/", json=payload)
            assert response.status_code == 403
            datapass_user_repository = resolve(DataPassUserRepository)
            user = await datapass_user_repository.get_by_email(email)
            assert user is None

            # With this token, request is authorized and user is registered...
            response = await client.post(
                "/auth/datapass/users/",
                json=payload,
                headers={"X-Signed-Token": token},
            )
            assert response.status_code == 201
            data = response.json()
            assert data == {
                "id": data["id"],
                "organization_siret": siret_1,
                "email": email,
                "role": "USER",
                "api_token": data["api_token"],
            }

            user = await datapass_user_repository.get_by_email(email)
            assert user is not None
            assert user.account.organization_siret == siret_1
            assert user.account.email == email
            assert user.account.role == UserRole.USER

    async def test_if_only_one_org_exists_then_creates_user_and_redirects_with_details(
        self, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bus = resolve(MessageBus)
        siret_1 = "11122233344441"
        siret_2 = "11122233344442"

        userinfo: DataPassUserInfo = {
            "email": "johndoe@mydomain.org",
            "organizations": [
                {
                    "siret": siret_1,
                    "label": "Organization 1",
                },
            ],
        }

        async with self._mock_openid_client(monkeypatch, userinfo):
            await bus.execute(CreateOrganizationFactory.build(siret=siret_1))
            await bus.execute(CreateOrganizationFactory.build(siret=siret_2))

            response = await client.get("/auth/datapass/callback/")
            assert response.status_code == 307

            datapass_user_repository = resolve(DataPassUserRepository)
            user = await datapass_user_repository.get_by_email("johndoe@mydomain.org")
            assert user is not None
            assert user.account.organization_siret == siret_1
            assert user.account.email == "johndoe@mydomain.org"
            assert user.account.role == UserRole.USER

            location = httpx.URL(response.headers["Location"])
            assert location.scheme == "http"
            assert location.netloc == b"client.testserver"
            assert location.path == "/auth/datapass/login"
            assert json.loads(location.params["user_info"]) == {
                "organization_siret": siret_1,
                "email": "johndoe@mydomain.org",
                "role": "USER",
                "api_token": user.account.api_token,
            }

    async def test_existing_password_user_reuses_account(
        self, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bus = resolve(MessageBus)

        email = "johndoe@mydomain.org"
        siret = "11122233344441"

        userinfo: DataPassUserInfo = {
            "email": email,
            "organizations": [{"siret": siret, "label": "Organization 1"}],
        }

        async with self._mock_openid_client(monkeypatch, userinfo):
            await bus.execute(CreateOrganizationFactory.build(siret=siret))
            await bus.execute(
                CreatePasswordUserFactory.build(organization_siret=siret, email=email)
            )
            account_repository = resolve(AccountRepository)
            existing_account = await account_repository.get_by_email(email)

            response = await client.get("/auth/datapass/callback/")
            assert response.status_code == 307

            datapass_user_repository = resolve(DataPassUserRepository)
            user = await datapass_user_repository.get_by_email("johndoe@mydomain.org")
            assert user is not None
            assert user.account == existing_account

    async def test_existing_password_user_in_different_org_is_error(
        self, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bus = resolve(MessageBus)

        email = "johndoe@mydomain.org"
        siret_1 = "11122233344441"
        siret_2 = "11122233344442"

        userinfo: DataPassUserInfo = {
            "email": email,
            "organizations": [{"siret": siret_2, "label": "Organization 2"}],
        }

        async with self._mock_openid_client(monkeypatch, userinfo):
            await bus.execute(CreateOrganizationFactory.build(siret=siret_1))
            await bus.execute(CreateOrganizationFactory.build(siret=siret_2))

            await bus.execute(
                CreatePasswordUserFactory.build(organization_siret=siret_1, email=email)
            )

            with pytest.raises(
                RuntimeError,
                match="requested to create a DataPassUser in different organization",
            ):
                await client.get("/auth/datapass/callback/")
