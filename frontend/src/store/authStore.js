import { create } from 'zustand';

export const useAuthStore = create((set, get) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  accessToken: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),

  setAuth: ({ user, access_token, refresh_token }) => {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', access_token);
    if (refresh_token) {
      localStorage.setItem('refresh_token', refresh_token);
    }
    set({
      user,
      accessToken: access_token,
      refreshToken: refresh_token || get().refreshToken,
      isAuthenticated: true,
    });
  },

  updateUser: (updatedUser) => {
    localStorage.setItem('user', JSON.stringify(updatedUser));
    set({ user: updatedUser });
  },

  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
  },
}));
