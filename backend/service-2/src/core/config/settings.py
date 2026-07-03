"""Application settings module."""

import json
from typing import Any

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings."""

    # 기본값(default)을 설정해두면 환경변수가 없을 때 사용됩니다.
    # 환경변수가 있으면 그 값이 우선순위를 가집니다.

    PROJECT_NAME: str
    DEBUG: bool = True
    DEFAULT_PORT: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_URL: str = "api/v1/auth/login"  # noqa: S105

    # Admin
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # Database (CQRS Pattern)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT_WRITE: int
    DB_PORT_READ: int
    DB_NAME: str

    # Write DB Session
    SQLALCHEMY_DATABASE_WRITE_URL: str | None = None
    # Read DB Session
    SQLALCHEMY_DATABASE_READ_URL: str | None = None

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        """DB 연결 URL을 조립합니다."""
        # 필수 DB 설정값이 모두 존재하는지 확인
        if self.DB_USER and self.DB_PASSWORD and self.DB_HOST and self.DB_NAME:
            # Write DB URL 조립
            if not self.SQLALCHEMY_DATABASE_WRITE_URL and self.DB_PORT_WRITE:
                self.SQLALCHEMY_DATABASE_WRITE_URL = (
                    f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT_WRITE}/{self.DB_NAME}"
                )

            # Read DB URL 조립
            if not self.SQLALCHEMY_DATABASE_READ_URL and self.DB_PORT_READ:
                self.SQLALCHEMY_DATABASE_READ_URL = (
                    f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT_READ}/{self.DB_NAME}"
                )

        return self

    # Observability
    TEMPO_EXPORTER: str | None = None
    LOKI_URL: str | None = None

    # Kafka Ecosystem
    KAFKA_BROKERS: list[str] | str
    KAFKA_TOPIC_ANALYSIS: str
    KAFKA_GROUP_ID: str

    KAFKA_CONNECT_URL: str | None
    SCHEMA_REGISTRY_URL: str | None
    KAFKA_REST_PROXY_URL: str | None

    @field_validator("KAFKA_BROKERS", mode="before")
    @classmethod
    def assemble_kafka_brokers(cls, v: Any) -> list[str]:
        """Kafka 브로커 목록을 조립합니다."""
        if isinstance(v, str):
            try:
                return json.loads(v)  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",") if i.strip()]
        return v  # type: ignore[no-any-return]

    # Redis & Automation
    REDIS_URL: str
    N8N_URL: str | None

    # Search & AI
    OPENSEARCH_URL: str | None
    OLLAMA_URL: str | None

    # CORS 설정 (문자열 또는 리스트 허용)
    CORS_ORIGINS: str | list[str] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str] | str:
        """CORS 허용 오리진을 조립합니다."""
        # Pydantic이 .env 값을 읽어서 v로 전달하므로 os.getenv 불필요
        if v is None or v == "":
            return []

        if isinstance(v, str):
            try:
                return json.loads(v)  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",") if i.strip()]
        return v  # type: ignore[no-any-return]

    # MinIO / S3 Config
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: str
    AWS_BUCKET_NAME: str

    # [중요] 외부 서빙용 URL (Nginx 주소)
    # docker-compose에서 http://localhost:80 으로 주입됨
    PUBLIC_ASSET_URL: str

    # Pydantic V2 설정
    # .env 파일을 자동으로 읽어오며, 대소문자를 구분하지 않습니다.
    # extra='ignore': 정의되지 않은 환경변수가 있어도 에러를 내지 않습니다.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
