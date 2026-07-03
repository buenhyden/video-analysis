"""Message Broker package."""

from src.core.message_broker.product_client import KafkaProducerClient

kafka_producer = KafkaProducerClient()

__all__ = ["KafkaProducerClient", "kafka_producer"]
