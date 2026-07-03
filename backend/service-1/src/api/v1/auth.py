import logging
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_write_db
from src.core.security import create_access_token, verify_password
from src.schemas import Token
from src.services import get_user_by_username

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/login", response_model=Token)  # type: ignore[misc]
async def login_access_token(
    db: Session = Depends(get_write_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # 로그인 시도 로깅 (정보보호를 위해 비밀번호는 로깅 금지)
    logger.info(f"Login attempt for user: {form_data.username}")

    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed for user: {form_data.username} - Invalid credentials")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)
    logger.info(f"Login successful for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
