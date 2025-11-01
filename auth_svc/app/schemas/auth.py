from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    jti: Optional[str] = None


class LoginRequest(SQLModel):
    email: str
    password: str


class RegisterRequest(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = None


class LogoutResponse(SQLModel):
    detail: str = "Logged out successfully."
