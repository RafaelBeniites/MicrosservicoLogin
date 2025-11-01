from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.core.config import settings
from app.models.token import RevokedToken
from app.models.user import User, UserRole
from app.schemas.auth import TokenPayload
from app.schemas.user import UserCreate

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == _normalize_email(email))
    return session.exec(statement).first()


def create_user(session: Session, data: UserCreate) -> User:
    if get_user_by_email(session, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        )

    user = User(
        email=_normalize_email(data.email),
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        role=data.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user."
        )
    return user


def create_access_token(*, subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"exp": expire, "sub": subject, "jti": uuid4().hex}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        token_payload = TokenPayload(**payload)
        if token_payload.jti is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing identifier.",
            )
        return token_payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def revoke_token(session: Session, payload: TokenPayload, *, user_id: Optional[int] = None) -> None:
    if payload.jti is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot revoke token without identifier.",
        )
    if is_token_revoked(session, payload.jti, auto_purge=False):
        return
    expires_at = (
        datetime.utcfromtimestamp(payload.exp)
        if payload.exp is not None
        else datetime.utcnow()
    )
    revoked = RevokedToken(jti=payload.jti, expires_at=expires_at, user_id=user_id)
    session.add(revoked)
    session.commit()


def is_token_revoked(session: Session, jti: Optional[str], *, auto_purge: bool = True) -> bool:
    if jti is None:
        return False
    revoked = session.get(RevokedToken, jti)
    if not revoked:
        return False
    if auto_purge and revoked.expires_at < datetime.utcnow():
        session.delete(revoked)
        session.commit()
        return False
    return True
