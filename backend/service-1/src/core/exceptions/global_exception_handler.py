"""Global Exception Handler Module."""

import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logger.app_logger import AppLogger

logger = AppLogger().setup(service_name="exception_handler")


async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """500 Internal Server Error를 처리합니다.

    Args:
        _: 사용되지 않는 Request 객체.
        exc: 발생한 예외 객체.
    """
    # 에러 스택 트레이스를 로그에 상세히 기록 (Request ID 포함됨)
    logger.error(f"Global Exception Handler Caught: {exc}")
    logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support.",
        },
    )
