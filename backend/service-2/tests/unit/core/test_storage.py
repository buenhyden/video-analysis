"""Tests for core.storage.minio_storage module."""

from io import BytesIO
from unittest.mock import MagicMock, patch

from src.core.storage.minio_storage import MinioStorage


def test_minio_storage_init():
    """Test MinioStorage initialization."""
    with patch("boto3.client") as mock_boto:
        storage = MinioStorage()
        assert storage.s3_client is not None
        mock_boto.assert_called_once()


def test_minio_storage_upload_file_success():
    """Test upload_file success path."""
    with patch("boto3.client") as mock_boto:
        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        storage = MinioStorage()

        file_obj = BytesIO(b"test data")
        result = storage.upload_file(file_obj, object_name="test.jpg")

        assert result is not None
        assert "test.jpg" in result
        mock_client.upload_fileobj.assert_called_once()


def test_minio_storage_upload_file_failure():
    """Test upload_file failure path."""
    from botocore.exceptions import ClientError

    with patch("boto3.client") as mock_boto:
        mock_client = MagicMock()
        mock_client.upload_fileobj.side_effect = ClientError(
            {"Error": {"Code": "500", "Message": "Error"}}, "upload_fileobj"
        )
        mock_boto.return_value = mock_client
        storage = MinioStorage()

        file_obj = BytesIO(b"test data")
        result = storage.upload_file(file_obj)

        assert result is None
