"""HTTP Exception Handler Module."""

import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException은 의도된 에러이므로 Warning 레벨로 로깅하거나 생략 가능."""
    logger.warning("HTTP Exception: %s (Status: %s)", exc.detail, exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
