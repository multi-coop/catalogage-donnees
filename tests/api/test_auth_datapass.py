import json
from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
import pytest
from starlette.requests import Request

import server.config.di
from server.config.di import configure, resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.repositories import DataPassUserRepository
from server.infrastructure.auth.datapass import DataPassOpenIDClient, DataPassUserInfo
from server.infrastructure.database import Database
from server.seedwork.application.di import Container
from server.seedwork.application.messages import MessageBus
from tests.factories import CreateOrganizationFactory


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

        siret_1 = "11122233344441"
        siret_2 = "11122233344442"

        userinfo: DataPassUserInfo = {
            "email": "johndoe@mydomain.org",
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
            orgs = json.loads(location.params["organizations"])
            assert orgs == [
                {"siret": siret_1, "name": "Organization 1"},
                {"siret": siret_2, "name": "Organization 2"},
            ]

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
            assert location.params["organization_siret"] == siret_1
            assert location.params["email"] == "johndoe@mydomain.org"
            assert location.params["role"] == "USER"
            assert location.params["api_token"] == user.account.api_token
