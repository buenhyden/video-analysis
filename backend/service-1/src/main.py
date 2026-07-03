"""Main App Module."""

import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# OpenTelemetry 관련 임포트
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.api import router
from src.core.cache import cache_client
from src.core.config import settings
from src.core.database import Base, engine_write, session_local_write
from src.core.exceptions import global_exception_handler, http_exception_handler
from src.core.logger import AppLogger
from src.core.message_broker import kafka_producer, kafka_notification_consumer

# ORM 등록 (Base.metadata.create_all을 위해 반드시 import 필요)
from src.infrastructure.orm import VideoORM, UserORM  # noqa: F401

# Kafka & Cache Import
from src.schemas import UserCreate
from src.services import create_user, get_user_by_username

# ---------------------------------------------------------
# Logging 설정
# ---------------------------------------------------------
app_logger = AppLogger()
app_logger.setup(
    service_name=settings.PROJECT_NAME,
    loki_url=settings.LOKI_URL,
    enable_console=True,
    enable_file=True,
    enable_loki=False,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# A. Tempo (Tracing) 설정
# ---------------------------------------------------------
# 서비스 이름 설정 (Grafana에서 이 이름으로 찾음)
resource = Resource(attributes={"service.name": settings.PROJECT_NAME})
# Trace Provider 설정
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
# Exporter 설정 (Docker의 Tempo gRPC 포트 4317로 전송)
# 로컬 실행 시: localhost, Docker 내부 실행 시: tempo
otlp_exporter = OTLPSpanExporter(endpoint=settings.TEMPO_EXPORTER, insecure=True)

# Span을 배치로 모아서 전송 (성능 최적화)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """애플리케이션 수명 주기 관리 (시작/종료)."""
    # ------------------------------------------------------------
    # [Startup] 애플리케이션 시작
    # ------------------------------------------------------------
    logger.info("🚀 Application startup...")
    # 1. Kafka & Redis Start
    await kafka_producer.start()
    await kafka_notification_consumer.start()
    await cache_client.start()

    # 2. Database Initialization
    logger.info("Initializing database...")
    # DB 테이블 생성 (Write Engine 사용)
    Base.metadata.create_all(bind=engine_write)

    db = session_local_write()
    try:
        user = get_user_by_username(db, settings.ADMIN_USERNAME)
        if not user:
            logger.info("Creating initial admin user...")
            logger.info("Creating initial admin user...")
            create_user(
                db,
                UserCreate(
                    username=settings.ADMIN_USERNAME,
                    password=settings.ADMIN_PASSWORD,
                ),
            )
        else:
            logger.info("Admin user already exists.")

    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        # 치명적인 오류라면 여기서 raise e를 하여 서버 시작을 중단할 수 있음
    finally:
        db.close()
        logger.info("Database initialization finished.")

    logger.info("✅ Application startup complete")

    yield
    # ------------------------------------------------------------
    # [Shutdown] 애플리케이션 종료
    # ------------------------------------------------------------
    logger.info("🛑 Application shutdown...")

    # Kafka & Redis Stop
    await kafka_notification_consumer.stop()
    await kafka_producer.stop()
    await cache_client.stop()

    logger.info("👋 Goodbye!")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
# ---------------------------------------------------------
# Middleware 설정
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)


@app.middleware("http")  # type: ignore[misc]
async def log_requests(request: Request, call_next: Callable[..., Any]) -> Response:
    """HTTP 요청 로깅 미들웨어."""
    # OTel Trace ID는 자동으로 로거 필터에 의해 주입됩니다.
    logger.info(f"Incoming Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Completed Request: {response.status_code}")
    return response


# ---------------------------------------------------------
# Exception Handler & Instrumentation
# ---------------------------------------------------------
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# FastAPI 자동 계측 (OpenTelemetry)
FastAPIInstrumentor.instrument_app(app)

# ---------------------------------------------------------
# Router
# ---------------------------------------------------------
app.include_router(router, prefix="/api")


@app.get("/")  # type: ignore[misc]
async def root() -> dict[str, str]:
    """Health Check Endpoint."""
    logger.info("Root endpoint access")
    return {"message": "Welcome to Video Portfolio API with Enhanced Logging"}
