"""Global exception handler module."""

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logger.app_logger import logger


async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """처리되지 않은 모든 예외(500 Internal Server Error)를 잡아서 처리합니다."""
    # 에러 스택 트레이스를 로그에 상세히 기록 (Request ID 포함됨)
    logger.error(f"Global Exception Handler Caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
