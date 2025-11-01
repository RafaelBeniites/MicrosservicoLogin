from typing import Optional

from sqlmodel import SQLModel

from app.models.user import UserRole


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.COLLABORATOR
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

