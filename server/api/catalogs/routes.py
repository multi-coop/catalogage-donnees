from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret
from server.application.catalogs.views import CatalogView
from server.config.di import resolve
from server.domain.catalogs.exceptions import CatalogAlreadyExists, CatalogDoesNotExist
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasAPIKey, IsAuthenticated
from .schemas import CatalogCreate

router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.post(
    "/",
    dependencies=[Depends(HasAPIKey())],
    response_model=CatalogView,
    status_code=201,
    responses={
        200: {},
    },
)
async def create_catalog(data: CatalogCreate) -> JSONResponse:
    bus = resolve(MessageBus)

    command = CreateCatalog(**data.dict())

    try:
        siret = await bus.execute(command)
    except CatalogAlreadyExists as exc:
        content = jsonable_encoder(CatalogView(**exc.catalog.dict()))
        return JSONResponse(content, status_code=200)

    query = GetCatalogBySiret(siret=siret)
    catalog = await bus.execute(query)
    content = jsonable_encoder(catalog)

    return JSONResponse(content, status_code=201)


@router.get("/{siret}/", dependencies=[Depends(IsAuthenticated())])
async def get_catalog(siret: Siret) -> CatalogView:
    bus = resolve(MessageBus)

    try:
        return await bus.execute(GetCatalogBySiret(siret=siret))
    except CatalogDoesNotExist as exc:
        raise HTTPException(404, detail=str(exc))
