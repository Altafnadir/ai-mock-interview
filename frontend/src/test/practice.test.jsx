import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import PracticePage from '../pages/candidate/PracticePage'
import { practiceApi } from '../api/practice'

vi.mock('../api/practice', () => ({
  practiceApi: {
    getDrills: vi.fn(),
  },
}))

describe('PracticePage Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state initially', () => {
    practiceApi.getDrills.mockReturnValue(new Promise(() => {}))

    render(
      <BrowserRouter>
        <PracticePage />
      </BrowserRouter>
    )

    expect(screen.getByText(/loading your personalized practice recommendations/i)).toBeInTheDocument()
  })

  it('renders drills when API returns recommendations and displays "Practice this" button', async () => {
    const mockDrills = [
      {
        id: 'drill-1',
        title: 'Targeted Articulation & Vocal Control Drill',
        tag: 'filler_words',
        duration: '5 Mins',
        desc: 'Practice answering technical questions with deliberate pacing and 1-second silent pauses.',
        category: 'Communication Exercise',
        is_personalized: true,
        score_context: 'Communication Score: 58%',
        suggested_topic: 'Communication & Articulation',
        suggested_category: 'Behavioral',
        suggested_role: 'Full Stack Developer',
        suggested_questions: ['Explain a challenging bug you fixed.'],
      },
    ]

    practiceApi.getDrills.mockResolvedValueOnce({ data: mockDrills })

    render(
      <BrowserRouter>
        <PracticePage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('Targeted Articulation & Vocal Control Drill')).toBeInTheDocument()
    })

    expect(screen.getByText(/communication score: 58%/i)).toBeInTheDocument()
    expect(screen.getByText(/personalized/i)).toBeInTheDocument()

    const practiceButton = screen.getByRole('button', { name: /practice this/i })
    expect(practiceButton).toBeInTheDocument()

    const link = practiceButton.closest('a')
    expect(link).toHaveAttribute(
      'href',
      '/interview/setup?topic=Communication%20%26%20Articulation&role=Full%20Stack%20Developer&category=Behavioral'
    )
  })

  it('renders error state when API call fails and provides retry button', async () => {
    practiceApi.getDrills.mockRejectedValueOnce({
      response: { data: { detail: 'Service temporarily unavailable' } },
    })

    render(
      <BrowserRouter>
        <PracticePage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/unable to load practice drills/i)).toBeInTheDocument()
    })

    expect(screen.getByText(/service temporarily unavailable/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /retry connection/i })).toBeInTheDocument()
  })

  it('renders empty state when drills list is empty', async () => {
    practiceApi.getDrills.mockResolvedValueOnce({ data: [] })

    render(
      <BrowserRouter>
        <PracticePage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/no practice drills available/i)).toBeInTheDocument()
    })

    expect(screen.getByRole('button', { name: /start an interview/i })).toBeInTheDocument()
  })
})
