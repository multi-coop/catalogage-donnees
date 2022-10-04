import re

from tools.makesecretkey import make_secret_key


def test_secretkey() -> None:
    secret_key = make_secret_key()
    assert len(secret_key) == 50

    assert re.search(r"[a-z]", secret_key)
    assert re.search(r"[0-9]", secret_key)

    special_characters = re.compile(r"[!@#\$%\^&\*\(-_=\+\)]")
    assert re.search(special_characters, secret_key)
