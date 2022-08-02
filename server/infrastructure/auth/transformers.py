from server.domain.auth.entities import User

from .models import UserModel


def update_instance(instance: UserModel, entity: User) -> None:
    for field in set(User.__fields__) - {"id"}:
        setattr(instance, field, getattr(entity, field))
