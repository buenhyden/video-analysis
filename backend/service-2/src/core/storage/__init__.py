"""Storage package."""

from src.core.storage.minio_storage import MinioStorage

storage_client = MinioStorage()

__all__ = ["MinioStorage", "storage_client"]
