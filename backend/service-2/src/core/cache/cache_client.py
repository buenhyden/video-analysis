"""Cache Client module."""

import json
import logging
from typing import Any

from redis.asyncio.cluster import RedisCluster

from src.core.config import settings

logger = logging.getLogger(__name__)


class CacheClient:
    """Redis Cache Client Wrapper."""

    _instance = None
    redis_client: RedisCluster[bytes] | None = None

    def __new__(cls) -> "CacheClient":
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def start(self) -> None:
        """앱 시작 시 Redis 연결."""
        try:
            self.redis_client = RedisCluster.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            # 연결 테스트
            await self.redis_client.ping()  # type: ignore[attr-defined]
            logger.info("Redis Cache connected.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def stop(self) -> None:
        """앱 종료 시 연결 해제."""
        if self.redis_client:
            await self.redis_client.aclose()  # type: ignore[attr-defined]
            logger.info("Redis Cache disconnected.")

    async def get(self, key: str) -> Any:
        """캐시 조회 (JSON 파싱 포함)."""
        if not self.redis_client:
            return None
        try:
            val = await self.redis_client.get(key)  # type: ignore[attr-defined]
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error(f"Cache GET error key={key}: {e}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """캐시 저장 (JSON 직렬화 포함, 기본 5분 유지)."""
        if not self.redis_client:
            return
        try:
            json_val = json.dumps(value, default=str)  # datetime 등 처리를 위해 default=str
            await self.redis_client.setex(key, ttl, json_val)  # type: ignore[attr-defined]
        except Exception as e:
            logger.error(f"Cache SET error key={key}: {e}")

    async def delete_pattern(self, pattern: str) -> None:
        """패턴에 맞는 키 삭제 (Invalidation 용)."""
        if not self.redis_client:
            return
        try:
            # SCAN을 사용하여 블로킹 없이 키 검색
            # SCAN을 사용하여 블로킹 없이 키 검색
            keys = [key async for key in self.redis_client.scan_iter(match=pattern)]  # type: ignore[attr-defined]

            if keys:
                await self.redis_client.delete(*keys)  # type: ignore[attr-defined]
                logger.info(f"Invalidated cache keys pattern: {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation error pattern={pattern}: {e}")
