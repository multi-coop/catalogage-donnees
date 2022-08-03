from starlette.datastructures import URL

from server.config.di import resolve
from server.config.settings import Settings


def get_client_root_url() -> URL:
    settings = resolve(Settings)
    return URL(settings.client_url)
