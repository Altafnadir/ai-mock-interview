import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import InterviewRoomPage from '../pages/candidate/InterviewRoomPage'
import { interviewApi } from '../api/interview'

vi.mock('../api/interview', () => ({
  interviewApi: {
    startSession: vi.fn(),
    getSession: vi.fn(),
    submitAnswer: vi.fn(),
    skipQuestion: vi.fn(),
    repeatQuestion: vi.fn(),
    endSession: vi.fn(),
    autosaveProgress: vi.fn(),
  }
}))

vi.mock('../store/toastStore', () => ({
  toast: {
    success: vi.fn(),
    warning: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
  }
}))

vi.mock('../utils/offlineStorage', () => ({
  bufferFailedAnswer: vi.fn().mockResolvedValue(1),
  getBufferedAnswers: vi.fn().mockResolvedValue([]),
  removeBufferedAnswer: vi.fn().mockResolvedValue(),
}))

describe('InterviewRoomPage Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Mock navigator.mediaDevices.getUserMedia
    if (!navigator.mediaDevices) {
      navigator.mediaDevices = {}
    }
    navigator.mediaDevices.getUserMedia = vi.fn().mockResolvedValue({
      getTracks: () => [{ stop: vi.fn() }],
    })
  })

  it('initializes interview room with media streams, timers, and question controls', async () => {
    interviewApi.startSession.mockResolvedValueOnce({ data: { status: 'in_progress' } })
    interviewApi.getSession.mockResolvedValueOnce({
      data: {
        id: 'sess-123',
        status: 'in_progress',
        questions: [
          { id: 'q-1', question_text: 'Explain how virtual DOM works in React.', time_limit_seconds: 120, source: 'ai' },
          { id: 'q-2', question_text: 'Describe a challenging bug you fixed.', time_limit_seconds: 120, source: 'ai' }
        ]
      }
    })

    render(
      <MemoryRouter initialEntries={['/interview/sess-123']}>
        <Routes>
          <Route path="/interview/:id" element={<InterviewRoomPage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Explain how virtual DOM works in React\./i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /repeat audio/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /skip question/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /next question/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /end now/i })).toBeInTheDocument()
    })
  })

  it('displays connection lost screen when session retrieval fails and does NOT load hardcoded questions', async () => {
    interviewApi.startSession.mockRejectedValueOnce(new Error('Network error connecting to interview server'))

    render(
      <MemoryRouter initialEntries={['/interview/sess-offline']}>
        <Routes>
          <Route path="/interview/:id" element={<InterviewRoomPage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Connection Lost/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Retry Connection/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Back to Dashboard/i })).toBeInTheDocument()
      // Ensure hardcoded fallback questions are NOT loaded
      expect(screen.queryByText(/Tell me about yourself/i)).not.toBeInTheDocument()
    })
  })

  it('retries connection when Retry Connection button is clicked', async () => {
    interviewApi.startSession.mockRejectedValueOnce(new Error('Initial failure'))
      .mockResolvedValueOnce({ data: { status: 'in_progress' } })
    interviewApi.getSession.mockResolvedValueOnce({
      data: {
        id: 'sess-offline',
        status: 'in_progress',
        questions: [{ id: 'q-recovered', question_text: 'Recovered interview question after retry?', time_limit_seconds: 90 }]
      }
    })

    render(
      <MemoryRouter initialEntries={['/interview/sess-offline']}>
        <Routes>
          <Route path="/interview/:id" element={<InterviewRoomPage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/Connection Lost/i)).toBeInTheDocument()
    })

    const retryBtn = screen.getByRole('button', { name: /Retry Connection/i })
    fireEvent.click(retryBtn)

    await waitFor(() => {
      expect(screen.getByText(/Recovered interview question after retry\?/i)).toBeInTheDocument()
    })
  })
})
