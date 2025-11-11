from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, LoginRequest
from app.schemas.token import Token
from app.crud.crud_user import get_by_email, create
import app.models  # noqa: F401 ensure model registry loaded
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    record_failed_login,
    is_locked_out,
    reset_failed_login,
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # Password policy
    if len(payload.password or "") < settings.PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters")
    if not any(c.isalpha() for c in payload.password) or not any(c.isdigit() for c in payload.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one letter and one digit")
    hashed_pw = get_password_hash(payload.password)
    user = create(db, payload, hashed_pw)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    key = f"login:{payload.email}"
    if is_locked_out(key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many failed login attempts. Try again later.")
    user = get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        record_failed_login(key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    reset_failed_login(key)
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 password grant compatible endpoint for Swagger Authorize button.
    Accepts form fields: username (email), password.
    """
    key = f"login:{form_data.username}"
    if is_locked_out(key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many failed login attempts. Try again later.")
    user = get_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        record_failed_login(key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    reset_failed_login(key)
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
