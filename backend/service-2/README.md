# 🎥 Video Analysis Worker

**Kafka 기반 비디오 분석 및 요약 서비스**

이 서비스는 Kafka 메시지를 통해 비디오 분석 요청을 수신하고, 비디오 프레임 추출, VLM(Vision Language Model)을 이용한 장면 설명, 그리고 LLM을 이용한 최종 요약을 수행하는 백그라운드 워커입니다.
추가적으로 요약된 내용을 바탕으로 AI 썸네일과 음성 브리핑(TTS)을 생성하여 제공합니다.

---

## ✨ 주요 기능

- **📨 Kafka Consumer**: `video.analysis.request` 토픽을 구독하여 분석 요청을 비동기로 처리합니다.
- **🎞️ 비디오 처리**: `yt-dlp`와 `OpenCV`를 사용하여 YouTube 및 기타 비디오 소스에서 키프레임을 추출합니다.
- **👁️ AI 비전 분석**: `Ollama` (minicpm-v:8b)를 사용하여 추출된 프레임의 내용을 텍스트로 설명합니다.
- **📝 AI 요약**: `Ollama` (exaone3.5)를 사용하여 장면 설명들을 종합하여 비디오 내용을 요약합니다.
- **🎨 AI 썸네일 생성**: 요약 내용을 바탕으로 프롬프트를 생성하고, `Pollinations.ai` (Flux/Turbo 모델)를 통해 고품질 썸네일 이미지를 생성합니다.
- **🗣️ AI 음성 브리핑**: `edge-tts`를 사용하여 요약된 텍스트를 자연스러운 한국어 음성(MP3)으로 변환합니다.
- **💾 스토리지 통합**: 생성된 썸네일과 오디오 파일을 MinIO(S3 호환 스토리지)에 자동으로 업로드합니다.
- **🔔 알림 시스템**: 분석 완료 시 Kafka를 통해 알림 이벤트를 발행합니다.
- **📊 관측성(Observability)**: `OpenTelemetry`와 `Loki`를 연동하여 분산 트레이싱 및 로그 모니터링을 지원합니다.

---

## 🛠️ 기술 스택

- **Language**: Python 3.12+
- **Package Manager**: uv
- **Framework**: Asyncio, AIOKafka
- **Video Processing**: OpenCV, yt-dlp
- **AI/ML Integration**: Ollama (MiniCPM-V, Exaone 3.5), Pollinations.ai
- **TTS**: edge-tts
- **Database**: PostgreSQL (SQLAlchemy)
- **Storage**: MinIO (boto3)
- **Observability**: OpenTelemetry, Loki
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

---

## 📂 프로젝트 구조 및 파일 분석

이 프로젝트는 확장성과 유지보수성을 고려하여 모듈화된 구조를 따르고 있습니다.

### Root Directory
- **`.agent/`**: AI 에이전트(`antigravity`)가 사용하는 메모리와 작업 내역을 저장하는 디렉토리입니다.
- **`.cursor/`**: Cursor IDE의 설정 및 프로젝트별 룰이 저장된 디렉토리입니다.
- **`.github/`**:
    - `workflows/`: CI/CD 파이프라인 정의 파일(`ci.yml`)이 위치합니다.
    - `instructions/`: AI 또는 개발자를 위한 가이드 문서가 포함될 수 있습니다.
- **`deploy/`**: Kubernetes 배포를 위한 설정 파일(`kustomization.yaml`, `overlays/`)이 위치합니다.
- **`docs/`**: 프로젝트 관련 문서들이 저장되는 디렉토리입니다.
- **`logs/`**: 로컬 실행 시 발생하는 로그 파일이 저장됩니다.
- **`src/`**: 소스 코드의 메인 디렉토리입니다.
- **`tests/`**: 테스트 코드가 위치합니다.
    - `unit/`: 단위 테스트.
    - `load/`: 부하 테스트(`locustfile.py` 등).

### 설정 파일 (Configuration Files)
- **`.pre-commit-config.yaml`**: 코드 품질 관리를 위한 pre-commit hook 설정입니다. `check-json`, `check-yaml`, `ruff`, `mypy`, `detect-secrets` 등의 훅이 정의되어 있어 커밋 전에 자동으로 검사를 수행합니다.
- **`.gitmessage`**: 일관된 커밋 메시지 작성을 위한 템플릿입니다. `<type> : <title>` 형식을 강제하며, Feat, Fix, Refactor 등 타입을 명시하도록 안내합니다.
- **`pyproject.toml`**: Python 프로젝트 설정 및 의존성 관리 파일입니다 (기존 `poetry`에서 `uv` 호환 구성 포함). Ruff, MyPy, Pytest 등의 툴 설정도 포함되어 있습니다.
- **`docker-compose.test.yml`**: 로컬 및 CI 환경에서 통합 테스트를 실행하기 위한 Docker Compose 설정입니다. PostgreSQL, Kafka, MinIO, Redis 등의 서비스와 함께 테스트 컨테이너를 실행합니다.

### 소스 코드 (`src/`)
- **`main.py`**: 서비스의 진입점(Entry point)입니다. Kafka Consumer를 시작합니다.
- **`core/`**: 핵심 공통 모듈입니다.
    - `config/`: 환경 변수 및 애플리케이션 설정 (`settings.py`).
- **`models/`**: 데이터베이스 스키마(SQLAlchemy 모델) 정의.
- **`services/`**: 핵심 비즈니스 로직.
    - `video_analysis.py`: 비디오 다운로드, 프레임 추출, AI 분석 오케스트레이션.
    - 기타 AI 및 스토리지 서비스 연동 로직 포함.

---

## 🚀 설치 및 실행 (Getting Started)

### 1. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 설정을 입력합니다.

```bash
cp .env.example .env
```

**주요 환경 변수:**
- `KAFKA_BROKERS`, `KAFKA_TOPIC_ANALYSIS`
- `OLLAMA_URL`
- `DATABASE_URL`
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`

### 2. 의존성 설치 및 로컬 실행 (using uv)

이 프로젝트는 패키지 관리자로 `uv`를 사용합니다.

```bash
# 의존성 동기화
uv sync

# 워커 실행
uv run python src/main.py
```

### 3. Docker 실행

```bash
docker-compose up --build
```

### 4. Git Hook 설정

```bash
# pre-commit 설치 및 설정
uv tool install pre-commit
pre-commit install
```
이제 `git commit` 시 자동으로 린트 및 포맷팅 검사가 수행됩니다.

### 5. 시크릿 관리 (Secret Management)

이 프로젝트는 `detect-secrets`를 사용하여 민감한 정보(API 키, 비밀번호 등)가 실수로 커밋되는 것을 방지합니다.

#### `.secrets.baseline` 파일이란?

`.secrets.baseline` 파일은 `detect-secrets`가 알려진(허용된) 시크릿의 베이스라인을 저장하는 파일입니다. 이 파일은:
- 프로젝트에 이미 존재하는 의도적인 시크릿 패턴을 기록합니다
- 예를 들어, 예제 설정 파일이나 테스트용 더미 값들을 포함할 수 있습니다
- Pre-commit hook이 이 베이스라인과 비교하여 새로운 시크릿만 감지합니다

#### 베이스라인 파일 생성 및 업데이트

```bash
# 초기 베이스라인 생성 (프로젝트 전체 스캔)
detect-secrets scan > .secrets.baseline

# 베이스라인 업데이트 (새로운 파일 추가 시)
detect-secrets scan --baseline .secrets.baseline
```

#### 새로운 시크릿 감지 시 대응

커밋 시 `detect-secrets`가 새로운 시크릿을 감지하면:

1. **실제 시크릿인 경우**:
   - 절대 커밋하지 마세요
   - `.env` 파일이나 환경 변수로 관리하세요
   - 이미 커밋한 경우 즉시 키를 교체하고 Git 히스토리에서 제거하세요

2. **False Positive (오탐)인 경우**:
   ```bash
   # 베이스라인에 추가 (허용 목록에 등록)
   detect-secrets scan --baseline .secrets.baseline

   # 변경사항 확인 후 커밋
   git add .secrets.baseline
   git commit
   ```

#### 주의사항

- `.secrets.baseline` 파일 자체는 **시크릿을 포함하지 않습니다** (해시값만 저장)
- 정기적으로 베이스라인을 검토하여 불필요한 항목을 제거하세요
- 실제 시크릿은 반드시 `.env` 파일에 저장하고, `.gitignore`에 추가하세요

---

## 🧪 테스트 (Testing)

### 단위 테스트 (Unit Tests)
`uv`를 통해 pytest를 실행합니다.

```bash
uv run pytest
```

### 통합 테스트 (Integration Tests via Docker)
Docker Compose를 사용하여 전체 인프라(DB, Kafka 등)를 띄우고 테스트를 수행합니다.

```bash
docker-compose -f docker-compose.test.yml run --rm test
```

---

## ⛓️ CI/CD (GitHub Actions)

`.github/workflows/ci.yml`에 정의된 워크플로우는 `main`, `develop` 브랜치에 푸시되거나 PR이 생성될 때 실행됩니다.

**주요 단계:**
1. **Checkout**: 코드를 체크아웃합니다.
2. **Setup uv**: 빠른 패키지 관리를 위해 `uv`를 설치합니다.
3. **Install Dependencies**: `uv sync`를 통해 의존성을 설치합니다.
4. **Pre-commit**: 전체 파일에 대해 린트 및 포맷 검사를 수행합니다 (`ruff`, `mypy` 등).
5. **Test (Docker)**: `docker-compose.test.yml`을 사용하여 통합 테스트 환경을 구축하고 테스트를 실행합니다.
