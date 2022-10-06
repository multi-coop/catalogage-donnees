import datetime as dt
import io
from typing import Any, Dict, Tuple

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.queries import GetCatalogBySiret, GetCatalogExport
from server.application.catalogs.views import CatalogView
from server.config.di import resolve
from server.domain.catalogs.exceptions import CatalogAlreadyExists, CatalogDoesNotExist
from server.domain.common.datetime import now
from server.domain.organizations.exceptions import OrganizationDoesNotExist
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasAPIKey, IsAuthenticated
from .rendering import to_csv
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
    except OrganizationDoesNotExist as exc:
        raise HTTPException(400, detail=str(exc))
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


export_cache: Dict[str, Tuple[dt.datetime, Any]] = {}


@router.get("/{siret}/export.csv")
async def export_catalog(siret: Siret) -> Response:

    max_age = dt.timedelta(days=1)
    cache_control_header = f"max-age={int(max_age.total_seconds())}"

    if siret in export_cache:
        expiry_date, content = export_cache[siret]

        if expiry_date > now():
            return Response(
                content,
                headers={
                    "content-type": "text/csv",
                    "X-Cache": "hit",
                    "Cache-Control": cache_control_header,
                },
            )
        else:
            del export_cache[siret]

    bus = resolve(MessageBus)

    try:
        export = await bus.execute(GetCatalogExport(siret=siret))
    except CatalogDoesNotExist as exc:
        raise HTTPException(404, detail=str(exc))

    f = io.StringIO()
    to_csv(export, f)
    content = f.getvalue()

    export_cache[siret] = (now() + max_age, content)

    return Response(
        content,
        headers={"content-type": "text/csv", "Cache-Control": cache_control_header},
    )
