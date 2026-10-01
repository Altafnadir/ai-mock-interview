import apiClient from './client';

export const reportApi = {
  getReport: (sessionId) => apiClient.get(`/reports/${sessionId}`),
  getPdfUrl: (sessionId) => `/api/v1/reports/${sessionId}/pdf`,
  getSummaryPdfUrl: (sessionId) => `/api/v1/reports/${sessionId}/summary-pdf`,
  getPosterUrl: (sessionId) => `/api/v1/reports/${sessionId}/poster`,
  shareReport: (sessionId) => apiClient.post(`/reports/${sessionId}/share`),
  getPublicReport: (token) => apiClient.get(`/public/reports/${token}`),
  revokeShare: (shareId) => apiClient.delete(`/reports/share/${shareId}`),
  emailReport: (sessionId) => apiClient.post(`/reports/${sessionId}/email`),
};
