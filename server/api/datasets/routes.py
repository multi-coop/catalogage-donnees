from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.responses import Response

from server.application.datasets.commands import (
    CreateDataset,
    DeleteDataset,
    UpdateDataset,
)
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.application.datasets.views import DatasetView
from server.config.di import resolve
from server.domain.auth.entities import UserRole
from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.specifications import DatasetSpec
from server.domain.organizations.exceptions import OrganizationDoesNotExist
from server.seedwork.application.messages import MessageBus

from ..auth.permissions import HasRole, IsAuthenticated
from . import filters
from .schemas import DatasetCreate, DatasetListParams, DatasetUpdate

router = APIRouter(prefix="/datasets", tags=["datasets"])

router.include_router(filters.router)


@router.get(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=Pagination[DatasetView],
)
async def list_datasets(
    params: DatasetListParams = Depends(),
) -> Pagination[DatasetView]:
    bus = resolve(MessageBus)

    page = Page(number=params.page_number, size=params.page_size)

    query = GetAllDatasets(
        page=page,
        spec=DatasetSpec(
            search_term=params.q,
            geographical_coverage__in=params.geographical_coverage,
            service__in=params.service,
            format__in=params.format,
            technical_source__in=params.technical_source,
            tag__id__in=params.tag_id,
            license=params.license,
        ),
    )

    return await bus.execute(query)


@router.get(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    responses={404: {}},
)
async def get_dataset_by_id(id: ID) -> DatasetView:
    bus = resolve(MessageBus)

    query = GetDatasetByID(id=id)
    try:
        return await bus.execute(query)
    except DatasetDoesNotExist:
        raise HTTPException(404)


@router.post(
    "/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    status_code=201,
)
async def create_dataset(data: DatasetCreate) -> DatasetView:
    bus = resolve(MessageBus)

    command = CreateDataset(**data.dict())

    try:
        id = await bus.execute(command)
    except OrganizationDoesNotExist as exc:
        raise HTTPException(400, detail=str(exc))

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


@router.put(
    "/{id}/",
    dependencies=[Depends(IsAuthenticated())],
    response_model=DatasetView,
    responses={404: {}},
)
async def update_dataset(id: ID, data: DatasetUpdate) -> DatasetView:
    bus = resolve(MessageBus)

    command = UpdateDataset(id=id, **data.dict())

    try:
        await bus.execute(command)
    except DatasetDoesNotExist:
        raise HTTPException(404)

    query = GetDatasetByID(id=id)
    return await bus.execute(query)


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
