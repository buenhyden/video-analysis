"""MinIO Storage Module."""

import logging
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError

from src.core.config import settings

# Backend의 경우: from app.core.config import settings

logger = logging.getLogger("core.storage")


class MinioStorage:
    """MinIO (S3 호환) 스토리지 관리 클래스."""

    def __init__(self) -> None:
        """S3 클라이언트를 초기화합니다."""
        # S3 호환 클라이언트 초기화
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.AWS_BUCKET_NAME

    def upload_file(
        self,
        file_obj: Any,
        object_name: str | None = None,
        content_type: str = "image/jpeg",
    ) -> str | None:
        """파일 객체(BytesIO 또는 UploadFile)를 MinIO에 업로드하고 외부에서 접근 가능한 Nginx URL을 반환합니다.

        URL은 http://localhost:80/portfolio-assets/abc.jpg 형태입니다.
        """
        if object_name is None:
            object_name = f"{uuid.uuid4()}.jpg"

        try:
            # 내부망을 통해 MinIO로 업로드
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket,
                object_name,
                ExtraArgs={"ContentType": content_type},
            )

            # DB에 저장할 URL은 Nginx(Public) 주소로 생성
            # 예: http://localhost:80/portfolio-assets/abc.jpg
            return f"{settings.PUBLIC_ASSET_URL}/{self.bucket}/{object_name}"

        except ClientError as e:
            logger.error("MinIO Upload Error: %s", e)
            return None
