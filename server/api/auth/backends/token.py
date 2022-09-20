from typing import Optional, Tuple

from fastapi.security.http import HTTPBearer
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from server.config.di import resolve
from server.domain.auth.repositories import AccountRepository

from ..models import ApiUser


class TokenAuthBackend(AuthenticationBackend):
    """
    Authenticate users based on their API token: 'Authorization: Bearer <api_token>'
    """

    security = HTTPBearer(scheme_name="Bearer", auto_error=False)

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, ApiUser]]:
        account_repository = resolve(AccountRepository)

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

        account = await account_repository.get_by_api_token(api_token)

        if account is None:
            raise AuthenticationError()

        return AuthCredentials(scopes=["authenticated"]), ApiUser(account)
