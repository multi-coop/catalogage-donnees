import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.application.auth.passwords import API_TOKEN_LENGTH
from server.domain.auth.entities import UserRole
from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:
    from ..organizations.models import OrganizationModel


class UserModel(Base):
    __tablename__ = "user"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    organization_siret: Siret = Column(
        CHAR(14),
        ForeignKey("organization.siret"),
        nullable=False,
    )
    organization: "OrganizationModel" = relationship(
        "OrganizationModel",
        back_populates="users",
    )
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False)
    api_token = Column(String(API_TOKEN_LENGTH), nullable=False)
