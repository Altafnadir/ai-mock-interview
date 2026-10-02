import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import LoginPage from '../pages/auth/LoginPage'
import { authApi } from '../api/auth'

vi.mock('../api/auth', () => ({
  authApi: {
    login: vi.fn(),
    requestOtp: vi.fn(),
    verifyOtpLogin: vi.fn(),
  }
}))

vi.mock('../store/toastStore', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  }
}))

describe('LoginPage Component', () => {
  it('renders login form elements with email and password inputs', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    expect(screen.getByText(/welcome back/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/candidate@gims\.edu\.pk/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/••••••••/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^sign in$/i })).toBeInTheDocument()
  })

  it('allows toggling between password login and passwordless OTP login', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    const otpTab = screen.getByRole('button', { name: /passwordless otp/i })
    fireEvent.click(otpTab)

    expect(screen.getByRole('button', { name: /send one-time code/i })).toBeInTheDocument()
  })

  it('submits credentials and calls authApi.login successfully', async () => {
    authApi.login.mockResolvedValueOnce({
      data: {
        access_token: 'fake-jwt',
        user: { id: 'u1', full_name: 'Test Student', email: 'candidate@gims.edu.pk', role: 'candidate' }
      }
    })

    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    fireEvent.change(screen.getByPlaceholderText(/candidate@gims\.edu\.pk/i), {
      target: { value: 'candidate@gims.edu.pk' }
    })
    fireEvent.change(screen.getByPlaceholderText(/••••••••/i), {
      target: { value: 'Secret123!' }
    })

    fireEvent.click(screen.getByRole('button', { name: /^sign in$/i }))

    await waitFor(() => {
      expect(authApi.login).toHaveBeenCalledWith({
        email: 'candidate@gims.edu.pk',
        password: 'Secret123!'
      })
    })
  })
})
