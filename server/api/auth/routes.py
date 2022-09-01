from fastapi import APIRouter, Depends, HTTPException

from server.api.types import APIRequest
from server.application.auth.commands import CreatePasswordUser, DeletePasswordUser
from server.application.auth.queries import GetAccountByEmail, LoginPasswordUser
from server.application.auth.views import AccountView, AuthenticatedAccountView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.exceptions import EmailAlreadyExists, LoginFailed
from server.domain.common.types import ID
from server.seedwork.application.messages import MessageBus

from . import datapass
from .permissions import HasRole, IsAuthenticated
from .schemas import PasswordUserCreate, PasswordUserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(datapass.router)


@router.post(
    "/users/",
    dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))],
    response_model=AccountView,
    status_code=201,
)
async def create_password_user(data: PasswordUserCreate) -> AccountView:
    bus = resolve(MessageBus)

    command = CreatePasswordUser(email=data.email, password=data.password)

    try:
        await bus.execute(command)
    except EmailAlreadyExists as exc:
        raise HTTPException(400, detail=str(exc))

    query = GetAccountByEmail(email=data.email)
    return await bus.execute(query)


@router.post("/login/", response_model=AuthenticatedAccountView)
async def login_password_user(data: PasswordUserLogin) -> AuthenticatedAccountView:
    bus = resolve(MessageBus)

    query = LoginPasswordUser(email=data.email, password=data.password)

    try:
        return await bus.execute(query)
    except LoginFailed as exc:
        raise HTTPException(401, detail=str(exc))


@router.get(
    "/users/me/",
    dependencies=[Depends(IsAuthenticated())],
)
async def get_connected_user(request: APIRequest) -> AccountView:
    return request.user.account


@router.delete(
    "/users/{id}/",
    dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))],
    status_code=204,
)
async def delete_password_user(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeletePasswordUser(account_id=id)
    await bus.execute(command)
