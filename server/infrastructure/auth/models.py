from typing import TYPE_CHECKING, Optional

from sqlalchemy import CHAR, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.application.auth.passwords import API_TOKEN_LENGTH
from server.domain.auth.entities import UserRole
from server.domain.common.types import ID
from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:
    from ..organizations.models import OrganizationModel


class AccountModel(Base):
    """
    Store information common to all user accounts.
    """

    __tablename__ = "account"

    id: ID = Column(UUID(as_uuid=True), primary_key=True)
    organization_siret: Siret = Column(
        CHAR(14),
        ForeignKey("organization.siret"),
        nullable=False,
    )
    organization: "OrganizationModel" = relationship(
        "OrganizationModel",
        back_populates="accounts",
    )
    email: str = Column(String, nullable=False, unique=True, index=True)
    role: UserRole = Column(Enum(UserRole, name="user_role_enum"), nullable=False)
    api_token: str = Column(String(API_TOKEN_LENGTH), nullable=False)

    password_user: Optional["PasswordUserModel"] = relationship(
        "PasswordUserModel", back_populates="account", uselist=False
    )
    datapass_user: Optional["DataPassUserModel"] = relationship(
        "DataPassUserModel", back_populates="account", uselist=False
    )


class PasswordUserModel(Base):
    """
    Store information specific to users that authenticate with email/password.
    """

    __tablename__ = "password_user"

    account_id: ID = Column(
        ForeignKey("account.id", ondelete="CASCADE"), primary_key=True
    )
    account: "AccountModel" = relationship(
        "AccountModel", back_populates="password_user", cascade="delete"
    )
    password_hash: str = Column(String, nullable=False)


class DataPassUserModel(Base):
    """
    Store information specific to users that authenticate with a DataPass account.
    """

    __tablename__ = "datapass_user"

    account_id: ID = Column(
        ForeignKey("account.id", ondelete="CASCADE"), primary_key=True
    )
    account: "AccountModel" = relationship(
        "AccountModel", back_populates="datapass_user", cascade="delete"
    )
