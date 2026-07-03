import { CONFIG } from '../config/constants';
import { MOCK_VIDEOS } from '../data/mockVideos';

export const apiService = {
  login: async (username, password) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      const res = await fetch(`${CONFIG.API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });
      if (!res.ok) throw new Error('로그인 실패: 아이디/비번을 확인하세요');
      return res.json();
    } catch (error) {
      console.warn('Login failed (backend unreachable?)', error);
      if (username === 'admin' && password === 'password') {
        return { access_token: 'demo_token', token_type: 'bearer' };
      }
      throw error;
    }
  },

  fetchVideos: async () => {
    try {
      const res = await fetch(`${CONFIG.API_URL}/videos/`);
      if (!res.ok) throw new Error('영상 목록 로딩 실패');
      return res.json();
    } catch (error) {
      console.warn('백엔드 연결 실패. Mock 데이터를 사용합니다.', error);
      return MOCK_VIDEOS;
    }
  },

  addVideo: async (video, token) => {
    const res = await fetch(`${CONFIG.API_URL}/videos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(video),
    });
    if (!res.ok) throw new Error('업로드 실패');
    return res.json();
  },

  deleteVideo: async (id, token) => {
    const res = await fetch(`${CONFIG.API_URL}/videos/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('삭제 실패');
    return true;
  },
  retryAnalysis: async (id, token) => {
    const res = await fetch(`${CONFIG.API_URL}/videos/${id}/analyze`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('재분석 요청 실패');
    return res.json();
  },
};
