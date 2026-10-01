import apiClient from './client';

export const practiceApi = {
  getDrills: () => apiClient.get('/practice/drills'),
  getQuestions: (params = {}) => apiClient.get('/practice/questions', { params }),
  getQuestion: (id) => apiClient.get(`/practice/questions/${id}`),
};
