import apiClient from './client';

export const resumeApi = {
  uploadResume: (formData) =>
    apiClient.post('/resumes', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getResumes: () => apiClient.get('/resumes'),
  getResumeById: (id) => apiClient.get(`/resumes/${id}`),
  replaceResume: (id, formData) =>
    apiClient.put(`/resumes/${id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  deleteResume: (id) => apiClient.delete(`/resumes/${id}`),
  analyzeResume: (id, payload) => apiClient.post(`/resumes/${id}/analyze`, payload),
  reanalyzeResume: (id) => apiClient.post(`/resumes/${id}/reanalyze`),
  getResumeAnalysis: (id) => apiClient.get(`/resumes/${id}/analysis`),
  getFullAnalysis: (id) => apiClient.get(`/resumes/${id}/analysis/full`),
};

