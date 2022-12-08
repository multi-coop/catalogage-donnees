from typing import Callable, Optional

import pytest
from pydantic import ValidationError

from server.domain.common.pagination import Page, Pagination


def test_default_page() -> None:
    page = Page()
    assert page.number == 1
    assert page.size == 10


@pytest.mark.parametrize(
    "pagefunc, exc",
    [
        pytest.param(
            lambda: Page(number=1),
            None,
            id="number-min",
        ),
        pytest.param(
            lambda: Page(number=0),
            ValidationError,
            id="number-min-exceeded",
        ),
        pytest.param(
            lambda: Page(number=-1),
            ValidationError,
            id="number-min-exceeded-neg",
        ),
        pytest.param(
            lambda: Page(number=10_000),
            None,
            id="number-max",
        ),
        pytest.param(
            lambda: Page(number=10_001),
            ValidationError,
            id="number-max-exceeded",
        ),
        pytest.param(
            lambda: Page(size=1),
            None,
            id="size-min",
        ),
        pytest.param(
            lambda: Page(size=0),
            ValidationError,
            id="size-min-exceeded",
        ),
        pytest.param(
            lambda: Page(size=-1),
            ValidationError,
            id="size-min-exceeded-neg",
        ),
        pytest.param(
            lambda: Page(size=100),
            None,
            id="size-max",
        ),
    ],
)
def test_page(pagefunc: Callable, exc: Optional[type]) -> None:
    if exc is None:
        pagefunc()
    else:
        with pytest.raises(exc):
            pagefunc()


def test_pagination_total_pages() -> None:
    items = [1, 2, 3]

    pagination = Pagination(items=items, total_items=0, page_size=3)
    assert pagination.total_pages == 0

    pagination = Pagination(items=items, total_items=2, page_size=3)
    assert pagination.total_pages == 1

    pagination = Pagination(items=items, total_items=3, page_size=3)
    assert pagination.total_pages == 1

    pagination = Pagination(items=items, total_items=4, page_size=3)
    assert pagination.total_pages == 2

    pagination = Pagination(items=items, total_items=7, page_size=3)
    assert pagination.total_pages == 3
