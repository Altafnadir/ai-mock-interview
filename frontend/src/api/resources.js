import apiClient from './client';

export const resourcesApi = {
  getRecommendations: () => apiClient.get('/recommendations'),
  getResources: (weakArea = '') =>
    apiClient.get('/resources', {
      params: weakArea ? { weak_area: weakArea } : {},
    }),
};
