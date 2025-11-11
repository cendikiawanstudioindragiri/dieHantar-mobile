from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.cache import get_redis
from app.db.session import get_db
from app.crud import crud_user

# Using pbkdf2_sha256 to avoid bcrypt backend issues in container; can migrate back to bcrypt later.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # pbkdf2_sha256 supports long passwords; optional max length guard can be added if desired.
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Hashing error: {e}")


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    # subject is user id as string
    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# Access helpers / decorators style utilities
def ensure_active(user):
    if not getattr(user, "is_active", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def require_active(user = Depends(get_current_user)):
    """Dependency for endpoints requiring an active user."""
    return ensure_active(user)


def require_feature(flag_name: str):
    """Factory returning a dependency that enforces a feature flag.

    Usage:
        @router.get("/some")
        def some_endpoint(_user=Depends(require_feature("ENABLE_EXPERIMENTAL_SEARCH"))):
            ...
    """
    def _dep(user = Depends(get_current_user)):
        flags = getattr(settings, "FEATURE_FLAGS", {}) or {}
        if not flags.get(flag_name, False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Feature '{flag_name}' disabled")
        return ensure_active(user)

    return _dep


def require_roles(*roles: str):
    """Dependency enforcing that current user has at least one of the given roles.

    Assumes `user` has attribute `roles` (list[str]) — if not present, denies.
    """
    def _dep(user = Depends(get_current_user)):
        user_roles = getattr(user, "roles", []) or []
        if not user_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No roles assigned")
        if not any(r in user_roles for r in roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return ensure_active(user)

    return _dep


# ---- Brute force / failed login tracking (Redis-backed with in-memory fallback) ----
_failed_login_store: dict[str, tuple[int, float]] = {}


def _now_ts() -> float:
    from time import time
    return time()


def record_failed_login(key: str) -> int:
    """Increment failed attempt counter for key (email or ip). Returns new count.
    Tries Redis first; falls back to process memory.
    """
    r = get_redis()
    if r:
        window = settings.LOGIN_LOCKOUT_SECONDS
        redis_key = f"auth:fail:{key}"
        try:
            pipe = r.pipeline()
            pipe.incr(redis_key)
            pipe.expire(redis_key, window)
            new_count, _ = pipe.execute()
            return int(new_count)
        except Exception:  # pragma: no cover
            pass
    # fallback
    now = _now_ts()
    window = settings.LOGIN_LOCKOUT_SECONDS
    entry = _failed_login_store.get(key)
    if not entry:
        _failed_login_store[key] = (1, now)
        return 1
    count, first_ts = entry
    if now - first_ts > window:
        _failed_login_store[key] = (1, now)
        return 1
    count += 1
    _failed_login_store[key] = (count, first_ts)
    return count


def reset_failed_login(key: str) -> None:
    r = get_redis()
    if r:
        try:
            r.delete(f"auth:fail:{key}")
        except Exception:  # pragma: no cover
            pass
    _failed_login_store.pop(key, None)


def is_locked_out(key: str) -> bool:
    r = get_redis()
    if r:
        try:
            val = r.get(f"auth:fail:{key}")
            if not val:
                return False
            return int(val) >= settings.MAX_LOGIN_ATTEMPTS
        except Exception:  # pragma: no cover
            pass
    entry = _failed_login_store.get(key)
    if not entry:
        return False
    count, first_ts = entry
    if count >= settings.MAX_LOGIN_ATTEMPTS:
        from time import time
        if time() - first_ts <= settings.LOGIN_LOCKOUT_SECONDS:
            return True
        reset_failed_login(key)
    return False
