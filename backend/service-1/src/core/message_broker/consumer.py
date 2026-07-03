"""service-1: Kafka Notification Consumer (Anti-Corruption Layer).

service-2가 발행한 분석 완료 이벤트를 수신하여
service-1 도메인 언어(AnalysisCompleted)로 변환 후 CompleteAnalysisUseCase에 위임한다.
"""

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from src.core.config import settings
from src.core.cache import cache_client
from src.core.database import session_local_write
from src.domain.video.events import AnalysisCompleted
from src.infrastructure.repositories.sqlalchemy_video_repository import SQLAlchemyVideoRepository
from src.application.video.complete_analysis import CompleteAnalysisUseCase

logger = logging.getLogger(__name__)


class KafkaNotificationConsumer:
    """service-2 분석 결과 수신 및 ACL 변환."""

    def __init__(self) -> None:
        self.consumer: AIOKafkaConsumer | None = None
        self.task: asyncio.Task | None = None
        self.topic = getattr(settings, "KAFKA_TOPIC_NOTIFICATION", "video-notifications")

    async def start(self) -> None:
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=settings.KAFKA_BROKERS,
            group_id="service-1-notification-consumer",
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        logger.info("service-1: Kafka Consumer started on topic '%s'", self.topic)
        self.task = asyncio.create_task(self._consume())

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()
        if self.consumer:
            await self.consumer.stop()
        logger.info("service-1: Kafka Consumer stopped")

    async def _consume(self) -> None:
        if not self.consumer:
            return
        try:
            async for msg in self.consumer:
                try:
                    payload = json.loads(msg.value.decode("utf-8"))
                    await self._handle(payload)
                except Exception as e:
                    logger.error("service-1: Error processing notification: %s", e)
        except asyncio.CancelledError:
            pass

    async def _handle(self, payload: dict) -> None:
        """ACL: service-2 페이로드 → AnalysisCompleted 도메인 이벤트 변환."""
        video_id = payload.get("video_id")
        status = payload.get("status")
        if not video_id or not status:
            return

        event = AnalysisCompleted(
            video_id=int(video_id),
            status=status,
            ai_summary=payload.get("ai_summary"),
            thumbnail_url=payload.get("thumbnail_url"),
            audio_url=payload.get("audio_url"),
        )

        db = session_local_write()
        try:
            repo = SQLAlchemyVideoRepository(db)
            use_case = CompleteAnalysisUseCase(repo)
            use_case.execute(event)
            await cache_client.delete_pattern("videos:list:*")
        finally:
            db.close()


kafka_notification_consumer = KafkaNotificationConsumer()
