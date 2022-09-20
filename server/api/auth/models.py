from typing import Optional

from starlette.authentication import BaseUser

from server.domain.auth.entities import Account


class ApiUser(BaseUser):
    def __init__(self, account: Optional[Account]) -> None:
        self._account = account

    @property
    def account(self) -> Account:
        if self._account is None:
            raise RuntimeError(
                "Cannot access .account, as the user is anonymous. "
                "Hint: did you forget to check for .is_authenticated?"
            )

        return self._account

    # Implement the 'BaseUser' interface.

    @property
    def is_authenticated(self) -> bool:
        return self._account is not None

    @property
    def display_name(self) -> str:
        return self._account.email if self._account is not None else ""
