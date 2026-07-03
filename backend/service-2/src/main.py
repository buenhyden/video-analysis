"""service-2: Main Entrypoint.

서비스 이름: Video Analysis Worker
역할: Kafka 소비 기반 AI 분석 파이프라인 실행
진입점: presentation/kafka_worker.py
"""

import asyncio
import logging

from src.core.config import settings
from src.core.logger import AppLogger
from src.core.message_broker import kafka_producer
from src.presentation.kafka_worker import run_worker

app_logger = AppLogger()
app_logger.setup(
    service_name=settings.PROJECT_NAME,
    loki_url=settings.LOKI_URL,
    enable_console=True,
    enable_file=True,
    enable_loki=False,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """service-2 시작."""
    logger.info("service-2: Starting Video Analysis Worker...")
    await kafka_producer.start()
    try:
        await run_worker()
    finally:
        await kafka_producer.stop()
        logger.info("service-2: Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
