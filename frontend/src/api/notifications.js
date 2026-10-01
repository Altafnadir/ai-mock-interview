import apiClient from './client';

export const notificationsApi = {
  getNotifications: () => apiClient.get('/notifications'),
  markAsRead: (id) => apiClient.put(`/notifications/${id}/read`),
  markAllAsRead: () => apiClient.put('/notifications/read-all'),
};
