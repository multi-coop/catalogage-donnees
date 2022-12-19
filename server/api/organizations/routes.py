from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.api.organizations.schemas import OrganizationCreate
from server.application.organizations.commands import CreateOrganization
from server.application.organizations.queries import GetOrganizationBySiret
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.domain.organizations.exceptions import OrganizationAlreadyExists
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasAPIKey

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post(
    "/",
    dependencies=[Depends(HasAPIKey())],
    response_model=OrganizationView,
    status_code=201,
    responses={
        200: {},
    },
)
async def create_organization_if_not_exists(
    data: OrganizationCreate,
) -> JSONResponse:
    bus = resolve(MessageBus)

    command = CreateOrganization(
        name=data.name, siret=data.siret, logo_url=data.logo_url
    )

    try:
        siret = await bus.execute(command)
    except OrganizationAlreadyExists as exc:
        content = jsonable_encoder(OrganizationView(**exc.organization.dict()))
        return JSONResponse(content, status_code=200)

    query = GetOrganizationBySiret(siret=siret)
    organization = await bus.execute(query)
    content = jsonable_encoder(organization)

    return JSONResponse(content, status_code=201)
