from pydantic import BaseModel, EmailStr, SecretStr


class PasswordUserCreate(BaseModel):
    email: EmailStr
    password: SecretStr


class PasswordUserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
