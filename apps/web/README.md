# Portfolio.io (hy-home.frontend)

**Portfolio.io**는 "Creative Motion & Visual Storytelling"을 주제로 한 영상 포트폴리오 웹 애플리케이션입니다. 사용자는 다양한 영상 프로젝트를 탐색하고 감상할 수 있으며, 관리자는 프로젝트를 등록하고 관리할 수 있습니다.

## 🌟 주요 기능 (Features)

- **포트폴리오 탐색**: 그리드 형태의 직관적인 UI로 영상 프로젝트를 한눈에 볼 수 있습니다.
- **검색 및 필터링**: 키워드 검색 및 카테고리별 필터링 기능을 제공하여 원하는 프로젝트를 쉽게 찾을 수 있습니다.
- **영상 재생**: 모달 창을 통해 끊김 없이 영상을 감상할 수 있습니다.
- **AI 분석 요약**: 각 영상에 대한 AI 기반의 심층 분석 요약을 제공합니다.
- **관리자 기능**:
  - 관리자 로그인 (Admin Access)
  - 새 프로젝트 등록 (제목, 카테고리, 설명, URL, 썸네일 등)
  - 프로젝트 삭제
- **반응형 디자인**: 데스크탑 및 모바일 환경 모두에 최적화된 디자인을 제공합니다.

## 🛠 기술 스택 (Tech Stack)

- **Frontend Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS, clsx, tailwind-merge
- **State Management**: Zustand (Persist middleware 사용)
- **Icons**: Lucide React
- **Code Quality**: ESLint, Prettier, Husky, Lint-staged

## 📂 프로젝트 구조 (Project Structure)

```
hy-home.frontend/
├── public/              # 정적 파일
├── src/
│   ├── assets/          # 이미지, 폰트 등 에셋
│   ├── components/      # 컴포넌트
│   │   ├── features/    # 기능별 컴포넌트 (admin, video 등)
│   │   ├── layout/      # 레이아웃 컴포넌트 (Navbar, Footer)
│   │   └── ui/          # 공통 UI 컴포넌트 (Modal, Toast 등)
│   ├── config/          # 설정 파일
│   ├── data/            # 정적 데이터
│   ├── pages/           # 페이지 컴포넌트 (Home.jsx)
│   ├── services/        # API 통신 로직
│   ├── store/           # 전역 상태 관리 (Zustand)
│   ├── utils/           # 유틸리티 함수
│   ├── App.jsx          # 메인 앱 컴포넌트
│   └── main.jsx         # 진입점
├── .env                 # 환경 변수
├── package.json         # 의존성 및 스크립트
└── vite.config.js       # Vite 설정
```

## 🚀 설치 및 실행 (Installation & Usage)

### 사전 요구 사항 (Prerequisites)

- Node.js (v18 이상 권장)
- npm 또는 yarn

### 설치 (Installation)

1. 저장소를 클론합니다.

   ```bash
   git clone <repository-url>
   cd hy-home.frontend
   ```

2. 의존성을 설치합니다.

   ```bash
   npm install
   ```

### 실행 (Development)

개발 서버를 실행합니다.

```bash
npm run dev
```

브라우저에서 `http://localhost:5173` (또는 터미널에 표시된 주소)으로 접속하여 확인합니다.

### 빌드 (Build)

배포를 위한 프로덕션 빌드를 생성합니다.

```bash
npm run build
```

### 린트 및 포맷팅 (Lint & Format)

코드 스타일을 확인하고 수정합니다.

```bash
npm run lint      # 린트 검사
npm run lint:fix  # 린트 자동 수정
npm run format    # 코드 포맷팅
```

## 📝 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.
