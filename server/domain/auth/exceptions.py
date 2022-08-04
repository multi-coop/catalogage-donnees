from ..common.exceptions import DoesNotExist


class AccountDoesNotExist(DoesNotExist):
    entity_name = "Account"


class EmailAlreadyExists(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email already exists: {email!r}")


class LoginFailed(Exception):
    pass
