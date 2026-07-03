import { useState } from 'react';

// Layout Components
import Footer from './components/layout/Footer';
import Navbar from './components/layout/Navbar';

// Page Components
import Home from './pages/Home';

// Feature Components (Global Modals)
import LoginModal from './components/features/admin/LoginModal';
import UploadModal from './components/features/admin/UploadModal';

function App()
{
  // 전역 모달의 열림/닫힘 상태 관리
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Navbar에 모달을 여는 함수를 props로 전달합니다.
        Navbar 내부에서 "Admin" 클릭 시 onOpenLogin 실행
        Navbar 내부에서 "New Project" 클릭 시 onOpenUpload 실행
      */}
      <Navbar
        onOpenLogin={() => setIsLoginOpen(true)}
        onOpenUpload={() => setIsUploadOpen(true)}
      />

      {/* 메인 페이지 컨텐츠 (Hero 섹션 + 비디오 그리드) */}
      <Home />

      {/* 푸터 */}
      <Footer />

      {/* 전역 모달 컴포넌트들 
        조건부 렌더링은 Modal 컴포넌트 내부(isOpen prop)에서 처리하거나, 
        여기서 {isLoginOpen && <LoginModal ... />} 형태로 처리할 수 있습니다.
        현재 Modal 구현은 내부에서 null을 리턴하는 방식이므로 항상 렌더링해둡니다.
      */}
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
      />

      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
      />
    </div>
  );
}

export default App;