"""Locust load test file."""

# tests/load/locustfile.py
import contextlib
import os
import socket
from datetime import UTC, datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from locust import HttpUser, between, events, task

# --- InfluxDB 설정 (Docker 환경변수에서 로드) ---
INFLUX_URL = f"http://{os.getenv('LOCUST_INFLUXDB_HOST', 'influxdb')}:8086"
INFLUX_TOKEN = os.getenv("LOCUST_INFLUXDB_TOKEN", "my-token")
INFLUX_ORG = os.getenv("LOCUST_INFLUXDB_ORG", "my-org")
INFLUX_BUCKET = os.getenv("LOCUST_INFLUXDB_BUCKET", "locust-bucket")

write_api = None
hostname = socket.gethostname()


@events.test_start.add_listener
def on_test_start(environment, **kwargs):  # noqa: ARG001
    """테스트 시작 시 InfluxDB 클라이언트 연결."""
    global write_api  # noqa: PLW0603
    with contextlib.suppress(Exception):
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):  # noqa: ARG001
    """요청 결과를 InfluxDB에 기록."""
    if write_api:
        point = (
            Point("locust_requests")
            .tag("result", "failure" if exception else "success")
            .field("response_time", response_time)
            .time(datetime.now(UTC))
        )
        with contextlib.suppress(Exception):
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)


class WebsiteUser(HttpUser):
    """Locust user class."""

    wait_time = between(1, 3)

    @task
    def index(self):
        """Root endpoint test task."""
        # 로컬 백엔드 서버 호출
        self.client.get("/")
