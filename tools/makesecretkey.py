"""
Cookie signing secret key generation tool.

Inspired by: https://github.com/RealOrangeOne/django-secret-key-generator/blob/master/src/ts/random.ts  # noqa
"""

import secrets

RAND_MAX = 2**8
CHARS = list("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
KEY_LENGTH = 50


def _generate_random_value(interval: range) -> int:
    sample_size = interval.start - interval.stop + 1
    upper = RAND_MAX - (RAND_MAX % sample_size)
    value = secrets.randbelow(upper)
    value %= sample_size
    return interval.start + value


def make_secret_key() -> str:
    return "".join(
        CHARS[_generate_random_value(range(len(CHARS)))] for _ in range(KEY_LENGTH)
    )


if __name__ == "__main__":
    print(make_secret_key())
