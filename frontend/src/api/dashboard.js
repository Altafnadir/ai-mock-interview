import apiClient from './client';

export const dashboardApi = {
  getOverview: () => apiClient.get('/dashboard/overview'),
  getTrends: () => apiClient.get('/dashboard/trends'),
  compareSessions: (ids) => apiClient.get(`/dashboard/compare?ids=${ids.join(',')}`),
};
