from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.schemas.auth import TokenPayload
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    payload: TokenPayload = auth_service.decode_token(token)
    if payload.sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )
    if auth_service.is_token_revoked(session, payload.jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked.",
        )
    user = auth_service.get_user_by_id(session, int(payload.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user
