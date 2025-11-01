from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.config import settings
from app.core.security import get_current_user, oauth2_scheme
from app.db.session import get_session
from app.models.user import UserRole
from app.schemas.auth import LoginRequest, LogoutResponse, RegisterRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services import auth_service

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
def register_user(
    payload: RegisterRequest, session: Session = Depends(get_session)
):
    role = payload.role.upper() if payload.role else UserRole.COLLABORATOR
    try:
        role_enum = UserRole(role)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid role. Use COLLABORATOR, IDEALIZER or ADMIN.",
        ) from exc
    user_create = UserCreate(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=role_enum,
    )
    return auth_service.create_user(session, user_create)


@router.post("/token", response_model=Token, tags=["auth"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = auth_service.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


@router.post("/login", response_model=Token, tags=["auth"])
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = auth_service.authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead, tags=["auth"])
def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout", response_model=LogoutResponse, tags=["auth"])
def logout(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    payload = auth_service.decode_token(token)
    auth_service.revoke_token(session, payload, user_id=current_user.id)
    return LogoutResponse()
