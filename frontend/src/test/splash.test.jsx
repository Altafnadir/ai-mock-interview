import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';
import SplashScreen, { hasSeenSplash, markSplashSeen, isDeepLinkRoute } from '../components/common/SplashScreen';

describe('SplashScreen Component', () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.clearAllTimers();
  });

  it('correctly identifies direct deep links that should bypass splash screen', () => {
    expect(isDeepLinkRoute('/shared/xyz789')).toBe(true);
    expect(isDeepLinkRoute('/interview/session-123/room')).toBe(true);
    expect(isDeepLinkRoute('/interview/session-123/processing')).toBe(true);
    expect(isDeepLinkRoute('/reports/rep-123')).toBe(true);

    expect(isDeepLinkRoute('/')).toBe(false);
    expect(isDeepLinkRoute('/login')).toBe(false);
    expect(isDeepLinkRoute('/dashboard')).toBe(false);
    expect(isDeepLinkRoute('/admin/login')).toBe(false);
  });

  it('renders splash screen on fresh browser session', () => {
    render(<SplashScreen currentPath="/" />);

    const splash = screen.getByRole('status');
    expect(splash).toBeInTheDocument();

    const logoImages = screen.getAllByAltText('Mock Interview AI');
    expect(logoImages.length).toBeGreaterThan(0);

    const skipButton = screen.getByRole('button', { name: /skip splash screen/i });
    expect(skipButton).toBeInTheDocument();
  });

  it('does NOT render when already seen in sessionStorage', () => {
    markSplashSeen();
    expect(hasSeenSplash()).toBe(true);

    const { container } = render(<SplashScreen currentPath="/" />);
    expect(container.firstChild).toBeNull();
  });

  it('does NOT render on deep link route', () => {
    const { container } = render(<SplashScreen currentPath="/shared/token-abc" />);
    expect(container.firstChild).toBeNull();
  });

  it('does NOT render on interview room route', () => {
    const { container } = render(<SplashScreen currentPath="/interview/session-123/room" />);
    expect(container.firstChild).toBeNull();
  });

  it('types the brand name and shows the tagline over time', () => {
    render(<SplashScreen currentPath="/" />);

    // Fast-forward through typewriter effect (~850ms to ~1800ms)
    act(() => {
      vi.advanceTimersByTime(1900);
    });

    expect(screen.getByText('Mock Interview AI')).toBeInTheDocument();
    expect(screen.getByText('Practice. Analyze. Get Hired.')).toBeInTheDocument();
  });

  it('skips immediately when Skip button is clicked', () => {
    const { container } = render(<SplashScreen currentPath="/" />);

    const skipBtn = screen.getByRole('button', { name: /skip splash screen/i });
    act(() => {
      fireEvent.click(skipBtn);
    });

    // Advance 300ms to allow exit transition
    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(container.firstChild).toBeNull();
    expect(hasSeenSplash()).toBe(true);
  });

  it('skips immediately when Escape key is pressed', () => {
    const { container } = render(<SplashScreen currentPath="/" />);

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    });

    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(container.firstChild).toBeNull();
    expect(hasSeenSplash()).toBe(true);
  });

  it('automatically finishes and unmounts after full animation sequence (~3s)', () => {
    const { container } = render(<SplashScreen currentPath="/" />);

    expect(container.firstChild).not.toBeNull();

    // Advance through the full sequence (2900ms+)
    act(() => {
      vi.advanceTimersByTime(3200);
    });

    expect(container.firstChild).toBeNull();
    expect(hasSeenSplash()).toBe(true);
  });
});
