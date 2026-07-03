import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { apiService } from '../services/api';

export const useStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      videos: [],
      isLoading: false,
      toast: { show: false, message: '', type: 'info' },

      showToast: (message, type = 'info') => {
        set({ toast: { show: true, message, type } });
        setTimeout(
          () => set((state) => ({ toast: { ...state.toast, show: false } })),
          3000
        );
      },

      login: async (username, password) => {
        try {
          const data = await apiService.login(username, password);
          set({
            token: data.access_token,
            user: { username },
            isAuthenticated: true,
          });
          get().showToast(`환영합니다, ${username}님!`, 'success');
          return true;
        } catch (err) {
          get().showToast(err.message, 'error');
          return false;
        }
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
        get().showToast('로그아웃 되었습니다.', 'info');
      },

      fetchVideos: async () => {
        set({ isLoading: true });
        try {
          const videos = await apiService.fetchVideos();
          set({ videos: videos.sort((a, b) => b.id - a.id), isLoading: false });
        } catch (err) {
          console.error(err);
          set({ isLoading: false });
        }
      },

      addVideo: async (videoData) => {
        const { token, showToast } = get();
        try {
          await apiService.addVideo(videoData, token);
          showToast('프로젝트가 등록되고 분석이 시작되었습니다.', 'success');
          get().fetchVideos();
        } catch (err) {
          console.error(err);
          showToast('등록에 실패했습니다 (서버 연결 확인 필요).', 'error');
        }
      },

      deleteVideo: async (id) => {
        const { token, videos, showToast } = get();
        try {
          await apiService.deleteVideo(id, token);
          set({ videos: videos.filter((v) => v.id !== id) });
          showToast('프로젝트가 삭제되었습니다.', 'success');
        } catch (err) {
          console.error(err);
          showToast('삭제에 실패했습니다.', 'error');
        }
      },
      retryAnalysis: async (id) => {
        const { token, showToast, videos } = get();
        try {
          await apiService.retryAnalysis(id, token);
          // 즉시 UI 상태 업데이트 (낙관적 업데이트)
          set({
            videos: videos.map((v) =>
              v.id === id ? { ...v, analysis_status: 'queued' } : v
            ),
          });
          showToast('재분석 요청이 대기열에 등록되었습니다.', 'success');
        } catch (err) {
          console.error(err);
          showToast('재분석 요청 실패', 'error');
        }
      },
    }),
    {
      name: 'portfolio-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
