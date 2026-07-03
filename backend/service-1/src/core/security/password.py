"""Password Utility Module."""

from datetime import datetime, timedelta
from typing import Any, cast

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    return cast(
        "str",
        jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM),
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    return cast("bool", pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Hash password."""
    return cast("str", pwd_context.hash(password))
