from typing import Callable

from ..auth.permissions import BasePermission
from ..types import APIRequest


class MatchesUserSiret(BasePermission):
    def __init__(self, key: Callable[[APIRequest], str]) -> None:
        super().__init__()
        self._key = key

    def has_permission(self, request: APIRequest) -> bool:
        if not request.user.is_authenticated:
            raise RuntimeError(
                "Running BelongsToOrganization but user is not authenticated. "
                "Hint: use IsAuthenticated() & BelongsToOrganization(...)"
            )

        user_siret = request.user.account.organization_siret
        claimed_siret = self._key(request)

        return user_siret == claimed_siret
