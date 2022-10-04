import re

from tools.makeapikey import make_api_key


def test_make_api_key() -> None:
    api_key = make_api_key()

    assert len(api_key) == 64
    assert re.search(r"[a-z]", api_key)
    assert re.search(r"[0-9]", api_key)
