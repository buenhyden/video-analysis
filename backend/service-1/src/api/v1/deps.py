"""Dependency Injection Module."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_read_db  # get_read_db 추가 import
from src.schemas import TokenPayload, User
from src.services import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


# 인증 확인은 최신 데이터 보장을 위해 Write DB(get_db)를 사용 권장
async def get_current_user(db: Session = Depends(get_read_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials validation failed") from e

    if token_data.sub is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token: missing subject")

    user = get_user_by_username(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
