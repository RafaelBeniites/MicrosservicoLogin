from __future__ import annotations

import enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRole(str, enum.Enum):
    COLLABORATOR = "COLLABORATOR"
    IDEALIZER = "IDEALIZER"
    ADMIN = "ADMIN"


class User(SQLModel, table=True):
    """Authentication entity representing a platform user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=120)
    role: UserRole = Field(default=UserRole.COLLABORATOR)
    is_active: bool = Field(default=True)

