from typing import Optional, Tuple

from fastapi.security.http import HTTPBearer
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from server.application.auth.queries import GetAccountByAPIToken
from server.config.di import resolve
from server.domain.auth.exceptions import AccountDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..models import ApiUser


class TokenAuthBackend(AuthenticationBackend):
    """
    Authenticate users based on their API token: 'Authorization: Bearer <api_token>'
    """

    security = HTTPBearer(scheme_name="Bearer", auto_error=False)

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        # NOTE: we don't reuse fastapi.security.HTTPBearer as it does not distinguish
        # "no Authorization" / "scheme is not Bearer" and "malformed Authorization".

        authorization = conn.headers.get("Authorization")

        if authorization is None:
            return AuthCredentials(), ApiUser(None)

        scheme, found, api_token = authorization.partition(" ")
        if not found:
            # Header is malformed -- that's a problem.
            raise AuthenticationError()

        if scheme.lower() != "bearer":
            return AuthCredentials(), ApiUser(None)

        bus = resolve(MessageBus)

        query = GetAccountByAPIToken(api_token=api_token)

        try:
            account = await bus.execute(query)
        except AccountDoesNotExist:
            raise AuthenticationError()

        return AuthCredentials(scopes=["authenticated"]), ApiUser(account)
