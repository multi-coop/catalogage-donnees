"""
Dependency injection (DI) setup.

Allows decoupling interfaces used by the application from their
concrete implementation, which might be configured on init.

Uses: https://punq.readthedocs.io/

Usage
-----

Register dependencies in `configure()` below.

The DI container should be initialized in entrypoints:

    ```python
    from server.config.di import bootstrap

    def main():
        ...

    if __name__ == "__main__":
        bootstrap()
        main()
    ```

You can then resolve dependencies elsewhere in the project,
e.g. in command or query handlers:

    ```python
    # server/application/todos/handlers.py
    from server.config.di import resolve
    from server.domain.todos.repositories import TodoRepository

    from .commands import CreateTodo

    async def create_todo(command: CreateTodo):
        repository = resolve(TodoRepository)
        ...
    ```

Or in routes:

    ```python
    # server/api/todos/routes.py
    from server.config.di import resolve
    from server.seedwork.application.messages import MessageBus
    from server.application.todos.commands import CreateTodo

    ...

    async def create_todo(...):
        bus = resolve(MessageBus)
        command = CreateTodo(...)
        todo = await bus.execute(command)
        ...
    ```

Or in any custom scripts as seems fit.
"""
import datetime as dt
from typing import Type, TypeVar

from server.application.auth.passwords import PasswordEncoder, Signer
from server.domain.auth.repositories import (
    AccountRepository,
    DataPassUserRepository,
    PasswordUserRepository,
)
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.dataformats.repositories import DataFormatRepository
from server.domain.datasets.repositories import DatasetRepository
from server.domain.extra_fields.repositories import ExtraFieldRepository
from server.domain.organizations.repositories import OrganizationRepository
from server.domain.tags.repositories import TagRepository
from server.infrastructure.adapters.messages import MessageBusAdapter
from server.infrastructure.auth.datapass import (
    DataPassOpenIDClient,
    get_datapass_openid_client,
)
from server.infrastructure.auth.passwords import (
    Argon2PasswordEncoder,
    ItsDangerousSigner,
)
from server.infrastructure.auth.repositories import (
    SqlAccountRepository,
    SqlDataPassUserRepository,
    SqlPasswordUserRepository,
)
from server.infrastructure.catalog_records.repositories import (
    SqlCatalogRecordRepository,
)
from server.infrastructure.catalogs.caching import ExportCache
from server.infrastructure.catalogs.repositories import SqlCatalogRepository
from server.infrastructure.database import Database
from server.infrastructure.dataformats.repositories import SqlDataFormatRepository
from server.infrastructure.datasets.repositories import SqlDatasetRepository
from server.infrastructure.extra_fields.repositories import SqlExtraFieldRepository
from server.infrastructure.organizations.repositories import SqlOrganizationRepository
from server.infrastructure.tags.repositories import SqlTagRepository
from server.seedwork.application.di import Container
from server.seedwork.application.messages import MessageBus
from server.seedwork.application.modules import load_modules

from .settings import Settings

T = TypeVar("T")

MODULES = [
    "server.infrastructure.datasets.module.DatasetsModule",
    "server.infrastructure.tags.module.TagsModule",
    "server.infrastructure.dataformats.module.DataFormatModule",
    "server.infrastructure.licenses.module.LicensesModule",
    "server.infrastructure.organizations.module.OrganizationsModule",
    "server.infrastructure.catalogs.module.CatalogsModule",
    "server.infrastructure.auth.module.AuthModule",
]


def configure(container: "Container") -> None:
    """
    Configure the Dependency Injection (DI) container.

    NOTE: Edit this as appropriate to register dependencies.
    """

    # Application-wide configuration

    settings = Settings()
    container.register_instance(Settings, settings)

    # Auth services
    container.register_instance(PasswordEncoder, Argon2PasswordEncoder())
    container.register_instance(Signer, ItsDangerousSigner(settings))
    container.register_instance(
        DataPassOpenIDClient, get_datapass_openid_client(settings)
    )

    # Event handling (Commands, queries, and the message bus)

    modules = load_modules(MODULES)

    command_handlers = {
        command: handler
        for cls in modules
        for command, handler in cls.command_handlers.items()
    }

    query_handlers = {
        query: handler
        for cls in modules
        for query, handler in cls.query_handlers.items()
    }

    bus = MessageBusAdapter(command_handlers, query_handlers)
    container.register_instance(MessageBus, bus)

    # Databases

    db = Database(url=settings.env_database_url, debug=settings.debug)
    container.register_instance(Database, db)

    # Repositories

    container.register_instance(AccountRepository, SqlAccountRepository(db))
    container.register_instance(PasswordUserRepository, SqlPasswordUserRepository(db))
    container.register_instance(DataPassUserRepository, SqlDataPassUserRepository(db))
    container.register_instance(CatalogRecordRepository, SqlCatalogRecordRepository(db))
    container.register_instance(DatasetRepository, SqlDatasetRepository(db))
    container.register_instance(TagRepository, SqlTagRepository(db))
    container.register_instance(OrganizationRepository, SqlOrganizationRepository(db))
    container.register_instance(CatalogRepository, SqlCatalogRepository(db))
    container.register_instance(DataFormatRepository, SqlDataFormatRepository(db))
    container.register_instance(ExtraFieldRepository, SqlExtraFieldRepository(db))

    # Caching
    container.register_instance(ExportCache, ExportCache(max_age=dt.timedelta(days=1)))


_CONTAINER = Container(configure)

bootstrap = _CONTAINER.bootstrap


def resolve(type_: Type[T]) -> T:
    # Allow monkeypatching `_CONTAINER` for overrides.
    return _CONTAINER.resolve(type_)
