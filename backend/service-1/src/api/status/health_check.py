"""Health Check API Module."""

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")  # type: ignore[misc]
async def health_check() -> dict[str, Any]:
    """간단한 상태 체크 엔드포인트.

    실제 구현 시 각 서비스(Redis, Kafka 등)에 ping을 날려 상태를 확인하는 로직 추가.
    """
    return {
        "status": "healthy",
        "services": {
            "kafka": "connected",
            "database": "connected",
            "redis": "connected",
            "ollama": "ready",
        },
    }
