"""MinIO Storage Client module."""

import logging
import uuid
from typing import Any

import boto3
import urllib3
from botocore.exceptions import ClientError

from src.core.config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("core.storage")


# ... (lines 4-14 remain same, but replacing top of file is easier if I just match top)
# actually I will just replace the class def and top docstring separately or together if close.
# detailed match:
class MinioStorage:
    """MinIO Storage Client."""

    def __init__(self) -> None:
        """S3 호환 클라이언트 초기화."""
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_ENDPOINT_URL,  # http://minio:9000 (내부 통신)
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            verify=False,
        )
        self.bucket = settings.AWS_BUCKET_NAME

    def upload_file(
        self, file_obj: Any, object_name: str | None = None, content_type: str = "image/jpeg"
    ) -> str | None:
        """파일 객체(BytesIO 또는 UploadFile)를 MinIO에 업로드하고 외부에서 접근 가능한 Nginx URL을 반환합니다."""
        if object_name is None:
            object_name = f"{uuid.uuid4()}.jpg"

        try:
            # 내부망을 통해 MinIO로 업로드
            self.s3_client.upload_fileobj(file_obj, self.bucket, object_name, ExtraArgs={"ContentType": content_type})

            # DB에 저장할 URL은 Nginx(Public) 주소로 생성
            return f"{settings.PUBLIC_ASSET_URL}/{self.bucket}/{object_name}"

        except ClientError as e:
            logger.error(f"MinIO Upload Error: {e}")
            return None
