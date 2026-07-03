import { Lock, LogOut, Play, Plus, Search } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { useStore } from '../store/useStore';

// Components
import AISummaryModal from '../components/features/video/AISummaryModal';
import VideoCard from '../components/features/video/VideoCard';
import VideoPlayerModal from '../components/features/video/VideoPlayerModal';
import Modal from '../components/ui/Modal';
import Toast from '../components/ui/Toast';

export default function Home() {
  const {
    videos,
    isAuthenticated,
    user,
    login,
    logout,
    fetchVideos,
    deleteVideo,
    addVideo,
    isLoading,
    retryAnalysis,
  } = useStore();

  const [search, setSearch] = useState('');
  const [filterCategory, setFilterCategory] = useState('All');
  const [activeVideo, setActiveVideo] = useState(null);
  const [summaryVideo, setSummaryVideo] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [uploadForm, setUploadForm] = useState({
    title: '',
    category: '',
    description: '',
    url: '',
    thumbnail: '',
  });

  useEffect(() => {
    fetchVideos();
    const interval = setInterval(fetchVideos, 10000);
    return () => clearInterval(interval);
    // [수정] 의존성 배열에 fetchVideos 추가 (Zustand 함수는 안정적이므로 무한 루프를 일으키지 않음)
  }, [fetchVideos]);

  const categories = useMemo(
    () => ['All', ...new Set(videos.map((v) => v.category))],
    [videos]
  );
  const filteredVideos = useMemo(() => {
    return videos.filter((v) => {
      const matchesSearch =
        v.title.toLowerCase().includes(search.toLowerCase()) ||
        v.description.toLowerCase().includes(search.toLowerCase());
      const matchesCategory =
        filterCategory === 'All' || v.category === filterCategory;
      return matchesSearch && matchesCategory;
    });
  }, [videos, search, filterCategory]);

  const handleLogin = async (e) => {
    e.preventDefault();
    if (await login(loginForm.username, loginForm.password)) {
      setLoginForm({ username: '', password: '' });
      setIsLoginOpen(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    await addVideo(uploadForm);
    setUploadForm({
      title: '',
      category: '',
      description: '',
      url: '',
      thumbnail: '',
    });
    setIsUploadOpen(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
      <Toast />

      <nav className="fixed top-0 z-40 w-full backdrop-blur-xl border-b border-white/5 bg-slate-950/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => window.scrollTo(0, 0)}
          >
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Play fill="white" size={14} className="ml-0.5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight text-white">
              Portfolio.io
            </span>
          </div>

          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <>
                <span className="hidden sm:block text-xs font-medium px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-slate-300">
                  <span className="text-indigo-400">●</span> {user?.username}
                </span>
                <button
                  onClick={() => setIsUploadOpen(true)}
                  className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-lg shadow-indigo-500/20"
                >
                  <Plus size={16} />{' '}
                  <span className="hidden sm:inline">New Project</span>
                </button>
                <button
                  onClick={logout}
                  className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                >
                  <LogOut size={18} />
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsLoginOpen(true)}
                className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors px-3 py-2 rounded-lg hover:bg-white/5"
              >
                <Lock size={16} /> Admin
              </button>
            )}
          </div>
        </div>
      </nav>

      <div className="relative pt-32 pb-20 sm:pt-40 sm:pb-24 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none opacity-50 mix-blend-screen" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700/50 backdrop-blur-md mb-8">
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-xs font-medium text-slate-300">
              AI Powered Analysis Available
            </span>
          </div>

          <h1 className="text-5xl sm:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-slate-500 mb-6 tracking-tight leading-tight">
            Creative Motion <br /> & Visual Storytelling
          </h1>
          <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
            브랜드의 가치를 시각적 언어로 통역합니다.
            <br className="hidden sm:block" />
            AI 기술을 활용한 심층적인 영상 분석과 인사이트를 제공합니다.
          </p>

          <div className="max-w-2xl mx-auto bg-slate-900/80 backdrop-blur-xl p-2 rounded-2xl border border-white/10 shadow-2xl flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1 group">
              <Search
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors"
                size={18}
              />
              <input
                type="text"
                placeholder="Search projects..."
                className="w-full bg-transparent border-none text-white placeholder-slate-500 pl-10 pr-4 py-2.5 focus:outline-none text-sm"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="flex gap-1 overflow-x-auto no-scrollbar pb-1 sm:pb-0 pl-2 sm:pl-0 sm:border-l border-white/10">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setFilterCategory(cat)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                    filterCategory === cat
                      ? 'bg-slate-700 text-white shadow-sm'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-32">
        {isLoading && videos.length === 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="bg-slate-900 rounded-2xl h-[400px] animate-pulse border border-slate-800"
              >
                <div className="h-[220px] bg-slate-800 rounded-t-2xl" />
                <div className="p-5 space-y-3">
                  <div className="h-6 bg-slate-800 rounded w-3/4" />
                  <div className="h-4 bg-slate-800 rounded w-full" />
                  <div className="h-4 bg-slate-800 rounded w-2/3" />
                </div>
              </div>
            ))}
          </div>
        ) : filteredVideos.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredVideos.map((video) => (
              <VideoCard
                key={video.id}
                video={video}
                isAdmin={isAuthenticated}
                onDelete={deleteVideo}
                onPlay={setActiveVideo}
                onShowSummary={setSummaryVideo}
                onRetry={retryAnalysis}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-32 border border-dashed border-slate-800 rounded-3xl bg-slate-900/30">
            <div className="inline-flex p-4 rounded-full bg-slate-800 mb-4 text-slate-500">
              <Search size={24} />
            </div>
            <p className="text-slate-400 text-lg font-medium">
              No projects found.
            </p>
            <button
              onClick={() => {
                setSearch('');
                setFilterCategory('All');
              }}
              className="mt-2 text-indigo-400 hover:text-indigo-300 text-sm"
            >
              Clear all filters
            </button>
          </div>
        )}
      </main>

      <footer className="border-t border-white/5 bg-slate-950 py-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-slate-500 text-sm">
            © 2025 Visual Portfolio. Built with FastAPI & React.
          </p>
        </div>
      </footer>

      <VideoPlayerModal
        video={activeVideo}
        isOpen={!!activeVideo}
        onClose={() => setActiveVideo(null)}
      />

      <AISummaryModal
        video={summaryVideo}
        isOpen={!!summaryVideo}
        onClose={() => setSummaryVideo(null)}
      />

      <Modal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        title="관리자 로그인"
      >
        <form onSubmit={handleLogin} className="space-y-4 p-6">
          <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-lg p-3 text-center">
            <span className="text-xs text-indigo-300">admin / password</span>
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">
              Username
            </label>
            <input
              type="text"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              value={loginForm.username}
              onChange={(e) =>
                setLoginForm({ ...loginForm, username: e.target.value })
              }
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">
              Password
            </label>
            <input
              type="password"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              value={loginForm.password}
              onChange={(e) =>
                setLoginForm({ ...loginForm, password: e.target.value })
              }
            />
          </div>
          <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 rounded-lg transition-all shadow-lg shadow-indigo-500/20">
            로그인
          </button>
        </form>
      </Modal>

      <Modal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        title="새 프로젝트 업로드"
      >
        <form onSubmit={handleUpload} className="space-y-4 p-6">
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">
              Project Title
            </label>
            <input
              required
              type="text"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 outline-none"
              value={uploadForm.title}
              onChange={(e) =>
                setUploadForm({ ...uploadForm, title: e.target.value })
              }
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">
                Category
              </label>
              <input
                required
                type="text"
                placeholder="Commercial"
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                value={uploadForm.category}
                onChange={(e) =>
                  setUploadForm({ ...uploadForm, category: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">
                Video URL (YouTube)
              </label>
              <input
                type="text"
                placeholder="https://youtube.com/..."
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                value={uploadForm.url}
                onChange={(e) =>
                  setUploadForm({ ...uploadForm, url: e.target.value })
                }
              />
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">
              Description
            </label>
            <textarea
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-indigo-500 outline-none h-24 resize-none"
              value={uploadForm.description}
              onChange={(e) =>
                setUploadForm({ ...uploadForm, description: e.target.value })
              }
            />
          </div>
          <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 rounded-lg transition-all shadow-lg shadow-indigo-500/20">
            프로젝트 등록
          </button>
        </form>
      </Modal>
    </div>
  );
}
