from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class RevokedToken(SQLModel, table=True):
    """Stores JWT identifiers that were explicitly revoked (logout)."""

    jti: str = Field(primary_key=True, max_length=64)
    expires_at: datetime = Field(nullable=False)
    revoked_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

