import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Logo from '../components/common/Logo'
import LoginPage from '../pages/auth/LoginPage'
import LandingPage from '../pages/public/LandingPage'
import Navbar from '../components/layout/Navbar'

// Mock zustand stores
vi.mock('../store/authStore', () => ({
  useAuthStore: vi.fn(() => ({
    user: { id: 'u1', full_name: 'Test Candidate', email: 'test@candidate.com', role: 'candidate' },
    isAuthenticated: true,
    logout: vi.fn(),
  })),
}))

vi.mock('../store/themeStore', () => ({
  useThemeStore: vi.fn(() => ({
    theme: 'dark',
    toggleTheme: vi.fn(),
  })),
}))

vi.mock('../store/toastStore', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}))

describe('Branding and Logo Components', () => {
  it('renders Logo component with default full horizontal variant', () => {
    render(
      <BrowserRouter>
        <Logo to="/" />
      </BrowserRouter>
    )

    const images = screen.getAllByAltText(/mock interview ai/i)
    expect(images.length).toBeGreaterThan(0)
    expect(images[0]).toHaveAttribute('src', expect.stringContaining('/brand/logo-full'))
  })

  it('renders Logo component with badge when specified', () => {
    render(
      <BrowserRouter>
        <Logo to="/admin" badge="Admin" />
      </BrowserRouter>
    )

    expect(screen.getByText('Admin')).toBeInTheDocument()
  })

  it('renders brand Logo on LoginPage', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    const logos = screen.getAllByAltText(/mock interview ai/i)
    expect(logos.length).toBeGreaterThan(0)
    expect(screen.getByText(/welcome back/i)).toBeInTheDocument()
  })

  it('renders brand Logo in Navbar layout', () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    )

    const navLogos = screen.getAllByAltText(/mock interview ai/i)
    expect(navLogos.length).toBeGreaterThan(0)
  })

  it('renders brand Logo on LandingPage navbar and footer', () => {
    render(
      <BrowserRouter>
        <LandingPage />
      </BrowserRouter>
    )

    const pageLogos = screen.getAllByAltText(/mock interview ai/i)
    // Should be present in both navbar and footer
    expect(pageLogos.length).toBeGreaterThanOrEqual(2)
  })
})
