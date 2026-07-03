# === Stage 1: "base" (공통 기반) ===
FROM python:3.13-slim as base
LABEL version="0.1" creator="chochyjj@gmail.com" description="Python 3.13"
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    TZ=Asia/Seoul

# 1. Timezone 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# 2. 시스템 의존성 설치 (빌드 및 런타임 공통)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3. uv 설치 (Docker 공식 이미지에서 바이너리만 복사)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# ==========================================
# Stage 2: Production Dependencies (프로덕션 의존성 빌드)
# ==========================================
FROM base AS prod-deps

# 의존성 파일 복사 (캐싱 활용)
COPY ./pyproject.toml ./uv.lock ./

# 프로덕션 의존성만 설치 (.venv 생성)
# --frozen: lockfile과 일치하도록 강제
# --no-install-project: 프로젝트 자체는 설치하지 않음 (의존성만)
# --no-dev: dev dependencies 제외
RUN uv sync --frozen --no-install-project --no-dev

# ==========================================
# Stage 3: Development Dependencies (개발 의존성 빌드)
# ==========================================
FROM prod-deps AS dev-deps

# 개발 의존성 포함 전체 설치 (.venv 업데이트)
RUN uv sync --frozen --no-install-project

# ==========================================
# Stage: Test (CI/CD 테스트용 이미지)
# ==========================================
FROM dev-deps AS test

WORKDIR /app
RUN mkdir /app/logs
# 소스 및 테스트 코드 복사
COPY ./src ./src
COPY ./tests ./tests
COPY .pre-commit-config.yaml .
COPY pyproject.toml .

# 테스트 실행을 위한 기본 설정 (필요시 오버라이드 가능)
CMD ["uv", "run", "pytest"]

# ==========================================
# Stage 4: Release (최종 배포용 이미지)
# ==========================================
FROM python:3.13-slim AS release

# 런타임 환경 변수
# uv가 생성한 .venv를 사용하기 위해 PATH 설정
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 1. 런타임 시스템 라이브러리 및 Timezone 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. 보안을 위한 비-루트 유저 생성
RUN useradd -m -s /bin/bash appuser
WORKDIR /app

# 3. prod-deps 단계에서 생성된 가상환경(.venv)만 복사
COPY --from=prod-deps --chown=appuser:appuser /app/.venv /app/.venv

# 4. 소스 코드 복사
COPY --chown=appuser:appuser ./src ./src

# 5. 유저 전환 및 실행
USER appuser
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# Stage 5: Dev (로컬 개발용 이미지)
# ==========================================
FROM dev-deps AS dev

# 개발 편의 도구 설치 (git, vim 등)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates default-libmysqlclient-dev git wget procps vim \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /app/scripts/
COPY .github/ ./.github/
COPY deploy/ ./deploy/
COPY ./README.md ./README.md
COPY ./.gitignore ./
COPY ./.dockerignore ./
COPY ./.pre-commit-config.yaml .
COPY ./.gitmessage .

# 가상환경 활성화 (PATH만으로도 충분하지만, 쉘 진입시 명시)
ENV PATH="/app/.venv/bin:$PATH"

# 소스 코드 복사 (Docker Compose 볼륨 마운트 사용 시 덮어씌워짐)
COPY ./src ./src

# 개발 모드 실행 (Reload 옵션 활성화)
# uv run으로 실행해도 되고, venv bindir이 PATH에 있으므로 직접 실행해도 됨
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
