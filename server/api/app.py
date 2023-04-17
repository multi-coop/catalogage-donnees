import sentry_sdk
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from server.config import Settings
from server.config.di import resolve

from .auth.middleware import AuthMiddleware
from .resources import auth_backend
from .routes import router

origins = [
    "http://localhost:3000",
]


class App(FastAPI):
    pass


def create_app(settings: Settings = None) -> App:
    if settings is None:
        settings = resolve(Settings)

    app = App(
        debug=settings.debug,
        title="API - catalogue.data.gouv.fr",
        version="0.1.0",  # Required by FastAPI, but meaningless for now.
        docs_url=settings.docs_url,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthMiddleware, backend=auth_backend)

    # Required by DataPass authlib OpenID client.
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

    if settings.debug:
        app.add_middleware(
            DebugToolbarMiddleware,
            panels=["server.api.debugging.debug_toolbar.panels.SQLAlchemyPanel"],
        )

    if settings.sentry_dsn is not None:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )

    app.include_router(router)

    return app
