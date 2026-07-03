"""Tests for core.exceptions modules."""

# HTTP status codes
import json
from unittest.mock import MagicMock

import pytest
from fastapi import Request
from starlette.exceptions import HTTPException

from src.core.exceptions.global_exception_handler import global_exception_handler
from src.core.exceptions.http_exception_handler import http_exception_handler

HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_ERROR = 500


@pytest.mark.asyncio
async def test_global_exception_handler():
    """Test global_exception_handler returns 500 JSONResponse."""
    request = MagicMock(spec=Request)
    exc = Exception("Test global error")

    response = await global_exception_handler(request, exc)

    assert response.status_code == HTTP_STATUS_INTERNAL_ERROR
    assert json.loads(response.body) == {"detail": "Internal Server Error"}


@pytest.mark.asyncio
async def test_http_exception_handler():
    """Test http_exception_handler returns correct JSONResponse."""
    request = MagicMock(spec=Request)
    exc = HTTPException(status_code=404, detail="Not Found")

    response = await http_exception_handler(request, exc)

    assert response.status_code == HTTP_STATUS_NOT_FOUND
    assert json.loads(response.body) == {"detail": "Not Found"}
