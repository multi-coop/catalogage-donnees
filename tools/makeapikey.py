import secrets


def make_api_key() -> str:
    return secrets.token_hex(32)


if __name__ == "__main__":
    print(make_api_key())
