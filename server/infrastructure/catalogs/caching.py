import datetime as dt
from typing import Callable, Dict, Optional, Tuple

from server.domain.common.datetime import now
from server.domain.organizations.types import Siret


class ExportCache:
    """
    Implement two types of cache to reduce the load associated to exporting catalogs:

    * Client-side caching, by adding 'Cache-Control' headers.
      Individual clients will only make new requests when their cache entry has expired.

    * Server-side caching, by storing exports in memory and reusing them for new
      clients until we consider them as stale (configurable).
    """

    def __init__(
        self, max_age: dt.timedelta, nowfunc: Callable[[], dt.datetime] = now
    ) -> None:
        self._exports: Dict[str, Tuple[dt.datetime, str]] = {}
        self._max_age = max_age
        self._cache_control = f"max-age={int(self._max_age.total_seconds())}"
        self._now = nowfunc

    def get(self, siret: Siret) -> Optional[str]:
        try:
            expiry_date, content = self._exports[siret]
        except KeyError:
            return None

        is_stale = self._now() > expiry_date

        if is_stale:
            del self._exports[siret]
            return None

        return content

    def set(self, siret: Siret, content: str) -> None:
        self._exports[siret] = (self._now() + self._max_age, content)

    @property
    def hit_headers(self) -> dict:
        return {"Cache-Control": self._cache_control, "X-Cache": "HIT"}

    @property
    def miss_headers(self) -> dict:
        return {"Cache-Control": self._cache_control}
