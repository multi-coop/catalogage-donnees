from typing import List, TypedDict

from authlib.common.security import generate_token
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from starlette.requests import Request
from starlette.responses import Response

from server.config.settings import Settings


class _UserInfoOrganization(TypedDict):
    siret: str
    label: str


class DataPassUserInfo(TypedDict):
    # The shape of this entry is documented here:
    # https://github.com/betagouv/api-auth/blob/7fe480f6000ebba4e25b54f01fb0a0ffe595937f/README.md#d%C3%A9tails-techniques  # noqa: E501
    # Only the fields we will be using are listed here.
    email: str
    organizations: List[_UserInfoOrganization]


class DataPassOpenIDClient:
    async def authorize_redirect(self, request: Request, callback_uri: str) -> Response:
        """
        Given our callback URI, trigger the authentication flow by redirecting to the
        Comptes DataPass authentication page.
        """
        raise NotImplementedError  # pragma: no cover

    async def authorize_userinfo(self, request: Request) -> DataPassUserInfo:
        """
        Given a request containing the authentication code, fetch the access token and
        return the result of the userinfo endpoint.

        Returns
        -------
        userinfo: dict
            A dictionary structured as documented here:
            https://github.com/betagouv/api-auth/blob/7fe480f6000ebba4e25b54f01fb0a0ffe595937f/README.md#d%C3%A9tails-techniques  # noqa: E501
        """
        raise NotImplementedError  # pragma: no cover


class _AuthlibDataPassOpenIDClient(DataPassOpenIDClient):
    def __init__(self, settings: Settings) -> None:
        # See: https://docs.authlib.org/en/latest/client/starlette.html#starlette-openid-connect # noqa: E501
        oauth = OAuth()

        # See: https://github.com/betagouv/api-auth/blob/7fe480f6000ebba4e25b54f01fb0a0ffe595937f/README.md  # noqa: E501
        oauth.register(
            name="datapass",
            client_id=settings.datapass_client_id,
            client_secret=settings.datapass_client_secret,
            server_metadata_url=(
                f"{settings.datapass_url}/.well-known/openid-configuration"
            ),
            client_kwargs={"scope": "openid email organizations"},
        )

        self._app: StarletteOAuth2App = oauth.datapass

    async def authorize_redirect(self, request: Request, callback_uri: str) -> Response:
        # TRICK TO WORK WITH DOCKER CONTAINERS :
        callback_uri = callback_uri.replace("http://localhost:3579", "https://catalogue.data.gouv.fr")
        return await self._app.authorize_redirect(
            request,
            callback_uri,
            # 'Comptes DataPass' OpenID Connect server requires a nonce, which we must
            # generate ourselves.
            # See: https://docs.authlib.org/en/latest/client/oauth2.html#oauth-2-openid-connect  # noqa: E501
            nonce=generate_token(),
        )

    async def authorize_userinfo(self, request: Request) -> DataPassUserInfo:
        token = await self._app.authorize_access_token(request)
        return await self._app.userinfo(token=token)


def get_datapass_openid_client(settings: Settings) -> DataPassOpenIDClient:
    return _AuthlibDataPassOpenIDClient(settings)
