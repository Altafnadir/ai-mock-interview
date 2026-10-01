import apiClient from './client';

export const resumeApi = {
  uploadResume: (formData) =>
    apiClient.post('/resumes', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getResumes: () => apiClient.get('/resumes'),
  getResumeById: (id) => apiClient.get(`/resumes/${id}`),
  deleteResume: (id) => apiClient.delete(`/resumes/${id}`),
  analyzeResume: (id) => apiClient.post(`/resumes/${id}/analyze`),
  getResumeAnalysis: (id) => apiClient.get(`/resumes/${id}/analysis`),
};
