import argon2
import itsdangerous
from pydantic import SecretStr

from server.application.auth.passwords import PasswordEncoder, Signer
from server.config.settings import Settings


class Argon2PasswordEncoder(PasswordEncoder):
    def __init__(self) -> None:
        self._hasher = argon2.PasswordHasher()

    def hash(self, password: SecretStr) -> str:
        return self._hasher.hash(password.get_secret_value())

    def verify(self, password: SecretStr, hash: str) -> bool:
        try:
            return self._hasher.verify(hash, password.get_secret_value())
        except argon2.exceptions.VerificationError:
            return False
        except argon2.exceptions.InvalidHash:
            return False


class ItsDangerousSigner(Signer):
    def __init__(self, settings: Settings) -> None:
        self._signer = itsdangerous.TimestampSigner(settings.secret_key)

    def sign(self, value: str) -> bytes:
        return self._signer.sign(value)

    def verify(self, data: bytes) -> bool:
        return self._signer.validate(data)
