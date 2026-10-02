import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import ResumePage from '../pages/candidate/ResumePage'
import { resumeApi } from '../api/resume'

vi.mock('../api/resume', () => ({
  resumeApi: {
    getResumes: vi.fn(),
    uploadResume: vi.fn(),
    replaceResume: vi.fn(),
    deleteResume: vi.fn(),
    analyzeResume: vi.fn(),
    getResumeAnalysis: vi.fn(),
  }
}))

vi.mock('../store/toastStore', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  }
}))

describe('ResumePage Component', () => {
  it('renders resume upload dropzone and document requirements', async () => {
    resumeApi.getResumes.mockResolvedValueOnce({ data: [] })

    render(<ResumePage />)

    await waitFor(() => {
      expect(screen.getByText(/resume intelligence manager/i)).toBeInTheDocument()
      expect(screen.getByText(/upload your resume \(pdf or docx\)/i)).toBeInTheDocument()
      expect(screen.getByText(/maximum file size: 5mb/i)).toBeInTheDocument()
    })
  })

  it('renders extracted skills and improvement suggestions when analysis is loaded', async () => {
    resumeApi.getResumes.mockResolvedValueOnce({
      data: [{
        id: 'res-101',
        original_filename: 'Candidate_CV.pdf',
        file_type: 'pdf',
        uploaded_at: '2026-10-01',
        is_active: true
      }]
    })

    resumeApi.getResumeAnalysis.mockResolvedValueOnce({
      data: {
        extracted_skills: ['FastAPI', 'React', 'Docker'],
        missing_skills: ['Kubernetes'],
        weak_sections: ['Project metrics'],
        improvement_suggestions: ['Add quantifiable KPIs to projects']
      }
    })

    render(<ResumePage />)

    await waitFor(() => {
      expect(screen.getByText(/Candidate_CV\.pdf/i)).toBeInTheDocument()
      expect(screen.getByText(/FastAPI/i)).toBeInTheDocument()
      expect(screen.getByText(/React/i)).toBeInTheDocument()
    })
  })
})
