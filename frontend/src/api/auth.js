import apiClient from './client';

export const authApi = {
  register: (data) => apiClient.post('/auth/register', data),
  verifyOtp: (data) => apiClient.post('/auth/verify-otp', data),
  resendOtp: (data) => apiClient.post('/auth/resend-otp', data),
  login: (data) => apiClient.post('/auth/login', data),
  googleLogin: (id_token) => apiClient.post('/auth/google', { id_token }),
  forgotPassword: (email) => apiClient.post('/auth/forgot-password', { email }),
  resetPassword: (data) => apiClient.post('/auth/reset-password', data),
  getMe: () => apiClient.get('/auth/me'),
  logout: (refreshToken) => apiClient.post('/auth/logout', { refresh_token: refreshToken }),
};
