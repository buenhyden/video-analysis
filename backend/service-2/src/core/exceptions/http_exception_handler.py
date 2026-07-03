"""HTTP exception handler module."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from src.core.logger.app_logger import logger


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException은 의도된 에러이므로 Warning 레벨로 로깅하거나 생략 가능합니다."""
    logger.warning(f"HTTP Exception: {exc.detail} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
