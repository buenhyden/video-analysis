"""App Logger Module."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# loki 라이브러리가 없을 경우를 대비한 처리 (선택사항)
try:
    from logging_loki import LokiHandler
except ImportError:
    LokiHandler = None

from opentelemetry import trace


class AppLogger:
    """애플리케이션 로거 설정 클래스입니다."""

    class _TraceIdFilter(logging.Filter):
        """OpenTelemetry Trace ID를 로그 레코드에 추가하는 필터."""

        def filter(self, record: logging.LogRecord) -> bool:
            span = trace.get_current_span()
            if span:
                span_context = span.get_span_context()
                if span_context != trace.INVALID_SPAN_CONTEXT:
                    record.trace_id = format(span_context.trace_id, "032x")
                else:
                    record.trace_id = "0"
            else:
                record.trace_id = "0"
            return True

    def setup(  # noqa: PLR0913
        self,
        service_name: str,
        loki_url: str | None = None,
        enable_console: bool = True,
        enable_file: bool = True,
        enable_loki: bool = False,
        log_file_path: str = "logs/app.log",
        log_level: int = logging.INFO,
    ) -> logging.Logger:
        """설정된 로거를 반환합니다.

        Args:
            service_name: 태깅을 위한 서비스 이름.
            loki_url: Loki URL (enable_loki가 True일 때 필수).
            enable_console: 콘솔 로깅 활성화 여부.
            enable_file: 파일 로깅 활성화 여부.
            enable_loki: Loki 로깅 활성화 여부.
            log_file_path: 로그 파일 경로 (기본값: logs/app.log).
            log_level: 로그 레벨 (기본값: INFO).

        Returns:
            설정된 root logger 객체.
        """
        # 루트 로거 가져오기 (이름 없이 호출)
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # 기존 핸들러 초기화 (중복 방지)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        # 핸들러에 부착할 필터 인스턴스 생성
        trace_filter = self._TraceIdFilter()

        # 1. Console Handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stderr)
            # Use uvicorn's default formatter if available, else standard
            formatter: logging.Formatter
            try:
                # pylint: disable=import-outside-toplevel
                from uvicorn.logging import DefaultFormatter  # noqa: PLC0415

                formatter = DefaultFormatter(
                    "%(levelprefix)s | %(asctime)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            except ImportError:
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            console_handler.setFormatter(formatter)
            console_handler.addFilter(trace_filter)  # ★ 여기 추가
            root_logger.addHandler(console_handler)

        # 2. File Handler
        if enable_file:
            log_dir = os.path.dirname(log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8",
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [TraceID: %(trace_id)s] - %(message)s"
            )
            file_handler.setFormatter(formatter)
            file_handler.addFilter(trace_filter)  # ★ 여기 추가
            root_logger.addHandler(file_handler)

        # 3. Loki Handler
        if enable_loki and loki_url:
            loki_handler = LokiHandler(
                url=loki_url,
                tags={"application": service_name},
                version="1",
            )
            loki_handler.addFilter(trace_filter)  # ★ 여기 추가
            root_logger.addHandler(loki_handler)
        elif enable_loki and not loki_url:
            sys.stderr.write("Warning: Loki logging enabled but no URL provided.\n")

        return root_logger
