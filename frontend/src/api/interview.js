import apiClient from './client';

export const interviewApi = {
  // Meta
  getJobRoles: () => apiClient.get('/meta/job-roles'),
  getCategories: () => apiClient.get('/meta/categories'),
  getDifficulties: () => apiClient.get('/meta/difficulties'),

  // Sessions
  createSession: (data) => apiClient.post('/interviews', data),
  getSession: (id) => apiClient.get(`/interviews/${id}`),
  startSession: (id) => apiClient.post(`/interviews/${id}/start`),
  getCurrentQuestion: (id) => apiClient.get(`/interviews/${id}/questions/current`),
  submitAnswer: (id, questionId, formData) =>
    apiClient.post(`/interviews/${id}/questions/${questionId}/answer`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  skipQuestion: (id, questionId) =>
    apiClient.post(`/interviews/${id}/questions/${questionId}/skip`),
  repeatQuestion: (id, questionId) =>
    apiClient.post(`/interviews/${id}/questions/${questionId}/repeat`),
  autosaveProgress: (id, data) => apiClient.post(`/interviews/${id}/progress`, data),
  endSession: (id) => apiClient.post(`/interviews/${id}/end`),
  getSessionStatus: (id) => apiClient.get(`/interviews/${id}/status`),
  getHistory: (params) => apiClient.get('/interviews', { params }),
  deleteSession: (id) => apiClient.delete(`/interviews/${id}`),
};
