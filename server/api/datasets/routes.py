import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.responses import Response

from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.exceptions import (
    CannotCreateDataset,
    CannotSeeDataset,
    CannotUpdateDataset,
)
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.application.datasets.views import DatasetView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.catalogs.exceptions import CatalogDoesNotExist
from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.specifications import DatasetSpec
from server.domain.extra_fields.entities import ExtraFieldValue
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasRole, IsAuthenticated
from ..types import APIRequest
from . import filters
from .schemas import DatasetCreate, DatasetListParams, DatasetUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/datasets", tags=["datasets"])

router.include_router(filters.router)


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=Pagination[DatasetView],
)
async def list_datasets(
    request: "APIRequest",
    params: DatasetListParams = Depends(),
) -> Pagination[DatasetView]:
    bus = resolve(MessageBus)

    page = Page(number=params.page_number, size=params.page_size)

    extra_field_value: Optional[ExtraFieldValue] = None

    if params.extra_field_value is not None:
        item = json.loads(params.extra_field_value)
        extra_field_value = ExtraFieldValue(**item)

    query = GetAllDatasets(
        page=page,
        spec=DatasetSpec(
            search_term=params.q,
            organization_siret=params.organization_siret,
            geographical_coverage__in=params.geographical_coverage,
            service__in=params.service,
            format__id__in=params.format_id,
            technical_source__in=params.technical_source,
            tag__id__in=params.tag_id,
            license=params.license,
            extra_field_value=extra_field_value,
        ),
        account=request.user.account,
    )

    return await bus.execute(query)


@router.get(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    responses={404: {}},
)
async def get_dataset_by_id(id: ID, request: "APIRequest") -> DatasetView:
    bus = resolve(MessageBus)

    query = GetDatasetByID(id=id, account=request.user.account)
    try:
        return await bus.execute(query)
    except DatasetDoesNotExist:
        raise HTTPException(404)
    except CannotSeeDataset as exec:
        logger.exception(exec)
        raise HTTPException(403, detail="Permission denied")


@router.post(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    status_code=201,
)
async def create_dataset(data: DatasetCreate, request: "APIRequest") -> DatasetView:
    bus = resolve(MessageBus)

    command = CreateDataset(account=request.user.account, **data.dict())

    try:
        id = await bus.execute(command)
    except CatalogDoesNotExist as exc:
        raise HTTPException(400, detail=str(exc))
    except CannotCreateDataset as exc:
        logger.exception(exc)
        raise HTTPException(403, detail="Permission denied")

    try:
        query = GetDatasetByID(id=id, account=request.user.account)
        return await bus.execute(query)
    except CannotSeeDataset as exec:
        logger.exception(exec)
        raise HTTPException(403, detail="Permission denied")


@router.put(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    responses={404: {}},
)
async def update_dataset(
    id: ID, data: DatasetUpdate, request: "APIRequest"
) -> DatasetView:
    bus = resolve(MessageBus)

    command = UpdateDataset(account=request.user.account, id=id, **data.dict())

    try:
        await bus.execute(command)
    except DatasetDoesNotExist:
        raise HTTPException(404)
    except CannotUpdateDataset as exc:
        logger.exception(exc)
        raise HTTPException(403, detail="Permission denied")

    try:
        query = GetDatasetByID(id=id, account=request.user.account)
        return await bus.execute(query)
    except CannotSeeDataset as exec:
        logger.exception(exec)
        raise HTTPException(403, detail="Permission denied")


@router.delete(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated() & HasRole(UserRole.ADMIN))],
    status_code=204,
    response_class=Response,
)
async def delete_dataset(id: ID) -> None:
    bus = resolve(MessageBus)

    command = DeleteDataset(id=id)
    await bus.execute(command)
