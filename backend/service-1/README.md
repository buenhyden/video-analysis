# hy-home.service-1

`hy-home.service-1`은 **FastAPI**를 기반으로 구축된 고성능 백엔드 마이크로서비스입니다. 이 서비스는 최신 Python 생태계 도구인 **uv**를 사용하여 의존성을 관리하며, **Kafka**, **Redis**, **PostgreSQL**과 같은 다양한 인프라 요소와 통합되어 있습니다.

## 🌟 주요 기능 (Key Features)

- **FastAPI 기반**: 비동기 처리를 통한 높은 성능과 자동 생성되는 API 문서(Swagger/ReDoc).
- **모던 Python 패키지 관리**: `uv`를 사용한 빠르고 효율적인 의존성 관리 및 가상환경 구성.
- **견고한 아키텍처**: 계층화된 아키텍처 (`api`, `core`, `services`, `schemas`, `models`) 적용.
- **통합 테스트 환경**: `docker-compose`를 활용한 데이터베이스 및 메시지 브로커 통합 테스트.
- **코드 품질 관리**: `pre-commit`, `ruff`, `mypy`를 통한 엄격한 린팅 및 타입 체크.
- **이벤트 기반 아키텍처**: Kafka를 활용한 비동기 메시징 처리 지원.

## 🛠 기술 스택 (Tech Stack)

- **Language**: Python 3.13
- **Web Framework**: FastAPI
- **Package Manager**: uv
- **Database**: PostgreSQL (Asyncpg)
- **Cache & Message Broker**: Redis, Kafka
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest, Locust (Load Testing)
- **CI/CD**: GitHub Actions

## 📋 사전 요구 사항 (Prerequisites)

이 프로젝트를 실행하기 위해서는 다음 도구들이 설치되어 있어야 합니다.

- **[Docker](https://www.docker.com/)** & **Docker Compose**
- **[uv](https://github.com/astral-sh/uv)** (Python 패키지 매니저)
  ```bash
  # Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## 🚀 설치 및 실행 (Installation & Getting Started)

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd hy-home.service-1
```

### 2. 가상환경 생성 및 의존성 설치
`uv`를 사용하여 가상환경을 생성하고 의존성을 동기화합니다.
```bash
uv sync
```

### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 설정을 수정합니다.
```bash
cp .env.example .env
```

### 4. 로컬 서버 실행
```bash
uv run uvicorn src.main:app --reload
```
서버가 실행되면 `http://localhost:8000/docs`에서 API 문서를 확인할 수 있습니다.

### 5. 도커 컴포즈를 통한 실행 (전체 인프라 포함)
개발용 DB 및 인프라와 함께 실행하려면 다음 명령어를 사용합니다.
```bash
docker compose -f docker-compose.test.yml up -d
```
> **참고**: `docker-compose.test.yml`은 테스트 및 로컬 개발용으로 구성된 PostgreSQL, Redis, Kafka 등을 포함합니다.

## 🧪 테스트 (Testing)

### 단위 및 통합 테스트
`pytest`를 사용하여 테스트를 수행합니다.
```bash
uv run pytest
```

### 부하 테스트 (Load Testing)
`locust`를 사용하여 부하 테스트를 수행할 수 있습니다.
```bash
# locust 실행
uv run locust -f tests/load/locustfile.py
```

## 🏗 프로젝트 구조 (Project Structure)

```plaintext
.
├── .github/            # GitHub Actions (CI/CD) 및 문서
├── deploy/             # 배포 관련 설정 (Kustomize 등)
├── docs/               # 프로젝트 문서
├── logs/               # 로그 파일 저장소
├── src/                # 소스 코드
│   ├── api/            # API 라우터 및 엔드포인트
│   ├── core/           # 핵심 설정, 보안, 유틸리티
│   ├── models/         # 데이터베이스 모델 (ORM)
│   ├── schemas/        # Pydantic 스키마 (DTO)
│   ├── services/       # 비즈니스 로직
│   └── main.py         # 애플리케이션 진입점
├── tests/              # 테스트 코드
│   ├── unit/           # 단위 테스트
│   └── load/           # 부하 테스트 (Locust)
├── .pre-commit-config.yaml # 코드 품질 관리 훅 설정
├── .gitmessage         # Git 커밋 메시지 템플릿
├── pyproject.toml      # 프로젝트 설정 및 의존성
└── uv.lock             # 의존성 잠금 파일
```

## 🧹 코드 품질 및 기여 가이드 (Code Quality & Contribution)

### Pre-commit Hooks
이 프로젝트는 코드 품질을 유지하기 위해 `pre-commit`을 사용합니다. 커밋 시 자동으로 실행되며, 다음 도구들을 포함합니다:
- **Ruff**: 린팅 및 포매팅
- **Mypy**: 정적 타입 검사
- **Interrogate**: 문서화 커버리지 체크
- **Checkers**: JSON, YAML, TOML 문법 검사 및 대용량 파일 체크

로컬에서 수동으로 실행하려면:
```bash
uv run pre-commit run --all-files
```

### Secrets Management (.secrets.baseline)
이 프로젝트는 **detect-secrets**를 사용하여 코드베이스에 실수로 커밋될 수 있는 시크릿(비밀번호, API 키 등)을 탐지합니다.

#### `.secrets.baseline` 파일이란?
`.secrets.baseline`은 detect-secrets가 생성하는 베이스라인 파일로, 다음과 같은 정보를 포함합니다:
- 알려진 시크릿 패턴들의 해시값
- False positive로 판단된 항목들
- 의도적으로 허용된 시크릿들 (예: 테스트용 더미 값)

#### 베이스라인 파일 생성 및 업데이트
새로운 코드를 추가하거나 시크릿이 변경되었을 때 베이스라인을 업데이트해야 합니다:
```bash
uv run detect-secrets scan > .secrets.baseline
```

#### Pre-commit Hook에서의 동작
커밋 시 detect-secrets는 자동으로 실행되어:
1. 새로운 시크릿이 감지되면 커밋을 차단
2. `.secrets.baseline`에 등록된 항목은 무시
3. False positive인 경우 베이스라인을 업데이트하여 허용 목록에 추가

#### False Positive 처리
정상적인 코드가 시크릿으로 오탐지되는 경우:
1. 베이스라인을 재생성: `uv run detect-secrets scan > .secrets.baseline`
2. 파일을 커밋에 포함하여 허용 목록에 추가
3. 또는 `# pragma: allowlist secret` 주석을 코드에 추가

### Git Commit Convention
일관된 커밋 메시지를 위해 `.gitmessage` 템플릿을 제공합니다.
```bash
git config commit.template .gitmessage
```
커밋 메시지 형식: `<type> : <subject>` (예: `feat : 사용자 로그인 기능 추가`)

## 🔄 CI/CD Pipeline

GitHub Actions를 통해 CI 파이프라인이 구성되어 있습니다 (`.github/workflows/ci.yml`).
주요 단계는 다음과 같습니다:
1. **Linting & Type Check**: `pre-commit`을 통한 코드 품질 검사.
2. **Build**: Docker 이미지 빌드 테스트.
3. **Integration Test**: `docker-compose`를 활용하여 실제 서비스(DB, Kafka 등)와 연동된 통합 테스트 수행.
