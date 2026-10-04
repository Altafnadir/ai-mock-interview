import apiClient from './client';

export const dashboardApi = {
  getOverview: () => apiClient.get('/dashboard/overview'),
  getPerformance: (range = 'week') => apiClient.get(`/dashboard/performance?range=${range}`),
  getRecommendation: () => apiClient.get('/dashboard/recommendation'),
  getTrends: () => apiClient.get('/dashboard/trends'),
  compareSessions: (ids) => apiClient.get(`/dashboard/compare?ids=${ids.join(',')}`),
};
