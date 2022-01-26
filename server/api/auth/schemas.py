from typing import Literal

from pydantic import BaseModel, EmailStr

from server.domain.common.types import ID


class UserRead(BaseModel):
    id: ID
    email: str


class UserCreate(BaseModel):
    email: EmailStr


class CheckAuthResponse(BaseModel):
    is_authenticated: Literal[True] = True