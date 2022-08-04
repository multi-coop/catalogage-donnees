from pydantic import EmailStr, SecretStr

from server.application.auth.views import AccountView, AuthenticatedAccountView
from server.seedwork.application.queries import Query


class LoginPasswordUser(Query[AuthenticatedAccountView]):
    email: EmailStr
    password: SecretStr


class GetAccountByEmail(Query[AccountView]):
    email: EmailStr


class GetAccountByAPIToken(Query[AccountView]):
    api_token: str
