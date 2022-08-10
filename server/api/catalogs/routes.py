from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret
from server.application.catalogs.views import CatalogView
from server.config.di import resolve
from server.domain.catalogs.exceptions import CatalogAlreadyExists
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasAPIKey
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

    command = CreateCatalog(organization_siret=data.organization_siret)

    try:
        siret = await bus.execute(command)
    except CatalogAlreadyExists as exc:
        content = jsonable_encoder(CatalogView(**exc.catalog.dict()))
        return JSONResponse(content, status_code=200)

    query = GetCatalogBySiret(siret=siret)
    catalog = await bus.execute(query)
    content = jsonable_encoder(catalog)

    return JSONResponse(content, status_code=201)
