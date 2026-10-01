import apiClient from './client';

export const adminApi = {
  // Dashboard & Analytics
  getDashboard: () => apiClient.get('/admin/dashboard'),
  getAnalytics: () => apiClient.get('/admin/analytics'),

  // Users
  getUsers: (params) => apiClient.get('/admin/users', { params }),
  getUserById: (id) => apiClient.get(`/admin/users/${id}`),
  updateUser: (id, data) => apiClient.put(`/admin/users/${id}`, data),
  toggleUserActive: (id, active) =>
    apiClient.put(`/admin/users/${id}/${active ? 'activate' : 'deactivate'}`),
  deleteUser: (id) => apiClient.delete(`/admin/users/${id}`),

  // Question Bank
  getQuestions: (params) => apiClient.get('/admin/questions', { params }),
  createQuestion: (data) => apiClient.post('/admin/questions', data),
  updateQuestion: (id, data) => apiClient.put(`/admin/questions/${id}`, data),
  deleteQuestion: (id) => apiClient.delete(`/admin/questions/${id}`),
  bulkUploadQuestions: (formData) =>
    apiClient.post('/admin/questions/bulk-upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  // Metadata Taxonomy
  getJobRoles: () => apiClient.get('/admin/job-roles'),
  createJobRole: (data) => apiClient.post('/admin/job-roles', data),
  updateJobRole: (id, data) => apiClient.put(`/admin/job-roles/${id}`, data),
  deleteJobRole: (id) => apiClient.delete(`/admin/job-roles/${id}`),

  getCategories: () => apiClient.get('/admin/categories'),
  createCategory: (data) => apiClient.post('/admin/categories', data),
  updateCategory: (id, data) => apiClient.put(`/admin/categories/${id}`, data),

  getDifficulties: () => apiClient.get('/admin/difficulties'),

  // Learning Resources & Feedback Templates
  getResources: () => apiClient.get('/admin/resources'),
  createResource: (data) => apiClient.post('/admin/resources', data),
  updateResource: (id, data) => apiClient.put(`/admin/resources/${id}`, data),
  deleteResource: (id) => apiClient.delete(`/admin/resources/${id}`),

  getFeedbackTemplates: () => apiClient.get('/admin/feedback-templates'),
  createFeedbackTemplate: (data) => apiClient.post('/admin/feedback-templates', data),
  updateFeedbackTemplate: (id, data) => apiClient.put(`/admin/feedback-templates/${id}`, data),
  deleteFeedbackTemplate: (id) => apiClient.delete(`/admin/feedback-templates/${id}`),

  // Sessions & Reports
  getSessions: (params) => apiClient.get('/admin/sessions', { params }),
  getSessionById: (id) => apiClient.get(`/admin/sessions/${id}`),
  deleteSession: (id) => apiClient.delete(`/admin/sessions/${id}`),

  getReports: (params) => apiClient.get('/admin/reports', { params }),
  getReportById: (id) => apiClient.get(`/admin/reports/${id}`),

  // Notifications Broadcast
  sendNotification: (data) => apiClient.post('/admin/notifications', data),

  // Monitoring & Logs
  getMonitoringStatus: () => apiClient.get('/admin/monitoring'),
  getLogs: (params) => apiClient.get('/admin/logs', { params }),

  // Security & Backup
  getLoginHistory: () => apiClient.get('/admin/security/login-history'),
  updateSecuritySettings: (data) => apiClient.put('/admin/security/settings', data),
  createBackup: () => apiClient.post('/admin/backup'),
  getBackups: () => apiClient.get('/admin/backups'),
  restoreBackup: (id) => apiClient.post(`/admin/restore/${id}`),
};
