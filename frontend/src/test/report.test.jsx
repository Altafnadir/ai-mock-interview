import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ReportPage from '../pages/candidate/ReportPage'
import { reportApi } from '../api/report'

vi.mock('../api/report', () => ({
  reportApi: {
    getReport: vi.fn(),
    getPdfUrl: vi.fn((id) => `/api/v1/reports/${id}/pdf`),
    getSummaryPdfUrl: vi.fn((id) => `/api/v1/reports/${id}/summary-pdf`),
    getPosterUrl: vi.fn((id) => `/api/v1/reports/${id}/poster`),
    shareReport: vi.fn(),
    getPublicReport: vi.fn(),
    revokeShare: vi.fn(),
    emailReport: vi.fn(),
  }
}))

vi.mock('../store/toastStore', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  }
}))

describe('ReportPage Component', () => {
  it('renders report metrics, score badges, action buttons, and recommendation sections', async () => {
    reportApi.getReport.mockResolvedValueOnce({
      data: {
        session_id: 'sess-100',
        overall_score: 88,
        final_verdict: 'Excellent',
        content_score: 90,
        communication_score: 85,
        confidence_score: 84,
        voice_score: 86,
        body_language_score: 82,
        grammar_score: 91,
        eye_contact_score: 88,
        candidate_snapshot: {
          full_name: 'Jane Candidate',
          job_role: 'Full Stack Developer',
          interview_category: 'Technical',
          difficulty: 'Intermediate'
        },
        strengths: ['Outstanding algorithmic explanations', 'Maintained strong eye contact'],
        weaknesses: ['Moderate filler word usage on behavioral questions'],
        recommendations: [
          {
            weak_area_tag: 'filler_words',
            practice_suggestion: 'Pause silently rather than using "um" or "like".',
            resource: {
              title: 'Mastering the Pause in Job Interviews',
              url: 'https://www.youtube.com/watch?v=sample'
            }
          }
        ]
      }
    })

    render(
      <MemoryRouter initialEntries={['/reports/sess-100']}>
        <Routes>
          <Route path="/reports/:sessionId" element={<ReportPage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Mock Interview Evaluation Report/i)).toBeInTheDocument()
      expect(screen.getByText(/Performance Breakdown & Insights/i)).toBeInTheDocument()
      expect(screen.getByText(/Printable Copy/i)).toBeInTheDocument()
      expect(screen.getByText(/Share Link/i)).toBeInTheDocument()
      expect(screen.getByText(/Email Report/i)).toBeInTheDocument()
      expect(screen.getByText(/Outstanding algorithmic explanations/i)).toBeInTheDocument()
    })
  })
})

