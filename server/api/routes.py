from fastapi import APIRouter, Depends, Request
from starlette.datastructures import URLPath
from starlette.responses import RedirectResponse

from server.config import Settings
from server.config.di import resolve

from . import auth, catalogs, dataformats, datasets, licenses, organizations, tags

router = APIRouter()


@router.get("/", response_class=RedirectResponse, include_in_schema=False)
def index(
    request: Request, settings: Settings = Depends(lambda: resolve(Settings))
) -> str:
    return URLPath(settings.docs_url).make_absolute_url(request.base_url)


router.include_router(auth.router)
router.include_router(datasets.router)
router.include_router(tags.router)
router.include_router(licenses.router)
router.include_router(organizations.router)
router.include_router(catalogs.router)
router.include_router(dataformats.router)
