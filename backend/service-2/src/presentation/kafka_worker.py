"""service-2: Kafka Worker (Presentation / Entry Point).

service-1이 발행한 VideoQueued 이벤트를 소비하여
ProcessAnalysisTaskUseCase에 위임하고,
결과 AnalysisCompleted 이벤트를 Kafka로 발행한다.
"""

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from src.core.config import settings
from src.core.message_broker import kafka_producer
from src.application.process_analysis_task import ProcessAnalysisTaskUseCase

logger = logging.getLogger(__name__)


async def run_worker() -> None:
    """service-2 메인 Kafka 소비 루프."""
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_ANALYSIS,
        bootstrap_servers=settings.KAFKA_BROKERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    logger.info(
        "service-2: Kafka Worker started. Listening on '%s'", settings.KAFKA_TOPIC_ANALYSIS
    )

    use_case = ProcessAnalysisTaskUseCase()
    topic_notification = getattr(settings, "KAFKA_TOPIC_NOTIFICATION", "video-notifications")

    try:
        async for msg in consumer:
            try:
                payload = json.loads(msg.value.decode("utf-8"))
                video_id = payload.get("video_id")
                video_url = payload.get("url")
                trace_id = payload.get("trace_id")

                if not video_id or not video_url:
                    logger.warning("service-2: Skipping message - missing video_id or url")
                    continue

                logger.info(
                    "service-2: Processing video %s (trace=%s)", video_id, trace_id
                )

                # 처리 시작 알림 (service-1 ACL에서 processing으로 업데이트)
                await kafka_producer.send_message(
                    topic_notification,
                    {"event": "analysis_processing", "video_id": video_id, "status": "processing"},
                )

                # 유스케이스 실행
                completed_event = await use_case.execute(
                    video_id=int(video_id), video_url=str(video_url)
                )

                # 완료 이벤트 발행 (service-1이 ACL로 수신)
                await kafka_producer.send_message(
                    topic_notification,
                    {
                        "event": f"analysis_{completed_event.status}",
                        "video_id": completed_event.video_id,
                        "status": completed_event.status,
                        "ai_summary": completed_event.ai_summary,
                        "thumbnail_url": completed_event.thumbnail_url,
                        "audio_url": completed_event.audio_url,
                    },
                )
                logger.info(
                    "service-2: Published AnalysisCompleted for video %s (status=%s)",
                    video_id,
                    completed_event.status,
                )

            except Exception as e:
                logger.error("service-2: Error processing message: %s", e)

    finally:
        await consumer.stop()
        logger.info("service-2: Kafka Worker stopped")
