from src.core.message_broker.product_client import KafkaProducerClient
from src.core.message_broker.consumer import kafka_notification_consumer

# 싱글톤 인스턴스
kafka_producer = KafkaProducerClient()

__all__ = ["KafkaProducerClient", "kafka_producer", "kafka_notification_consumer"]
