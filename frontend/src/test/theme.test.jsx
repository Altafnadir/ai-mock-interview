import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ThemeSwitcher from '../components/common/ThemeSwitcher';
import {
  useThemeStore,
  THEMES,
  applyThemeToDOM,
  getInitialTheme,
  setupSystemThemeListener,
} from '../store/themeStore';

describe('Theme System and ThemeSwitcher Component', () => {
  let listeners = [];

  beforeEach(() => {
    localStorage.clear();
    document.documentElement.className = '';
    document.documentElement.removeAttribute('data-theme');
    listeners = [];

    // Mock matchMedia implementation with event tracking
    window.matchMedia = vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn((fn) => listeners.push(fn)),
      removeListener: vi.fn(),
      addEventListener: vi.fn((event, fn) => {
        if (event === 'change') listeners.push(fn);
      }),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    useThemeStore.getState().setTheme(THEMES.SYSTEM);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('defaults to system theme when no valid preference is in localStorage', () => {
    expect(getInitialTheme()).toBe('system');
    const state = useThemeStore.getState();
    expect(state.theme).toBe('system');
    expect(document.documentElement.getAttribute('data-theme')).toBe('system');
  });

  it('safely falls back to system theme when localStorage contains an invalid value', () => {
    localStorage.setItem('mock_interview_theme', 'invalid_neon_theme_xyz');
    expect(getInitialTheme()).toBe('system');

    // Also testing setTheme with invalid input
    useThemeStore.getState().setTheme('nonexistent');
    expect(useThemeStore.getState().theme).toBe('system');
    expect(document.documentElement.getAttribute('data-theme')).toBe('system');
  });

  it('updates data-theme, removes dark class, and sets localStorage when white theme is selected', () => {
    useThemeStore.getState().setTheme(THEMES.WHITE);

    expect(useThemeStore.getState().theme).toBe('white');
    expect(localStorage.getItem('mock_interview_theme')).toBe('white');
    expect(document.documentElement.getAttribute('data-theme')).toBe('white');
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    const meta = document.querySelector('meta[name="theme-color"]');
    expect(meta?.getAttribute('content')).toBe('#FFFFFF');
  });

  it('updates data-theme, adds dark class, and sets localStorage when black theme is selected', () => {
    useThemeStore.getState().setTheme(THEMES.BLACK);

    expect(useThemeStore.getState().theme).toBe('black');
    expect(localStorage.getItem('mock_interview_theme')).toBe('black');
    expect(document.documentElement.getAttribute('data-theme')).toBe('black');
    expect(document.documentElement.classList.contains('dark')).toBe(true);

    const meta = document.querySelector('meta[name="theme-color"]');
    expect(meta?.getAttribute('content')).toBe('#000000');
  });

  it('updates data-theme, adds dark class, and sets localStorage when blue theme is selected', () => {
    useThemeStore.getState().setTheme(THEMES.BLUE);

    expect(useThemeStore.getState().theme).toBe('blue');
    expect(localStorage.getItem('mock_interview_theme')).toBe('blue');
    expect(document.documentElement.getAttribute('data-theme')).toBe('blue');
    expect(document.documentElement.classList.contains('dark')).toBe(true);

    const meta = document.querySelector('meta[name="theme-color"]');
    expect(meta?.getAttribute('content')).toBe('#0B1B3F');
  });

  it('system theme dynamically reflects OS prefers-color-scheme via matchMedia', () => {
    useThemeStore.getState().setTheme(THEMES.SYSTEM);

    let changeCallback;
    window.matchMedia = vi.fn().mockImplementation((query) => ({
      matches: false, // initial light
      media: query,
      addEventListener: vi.fn((event, handler) => {
        if (event === 'change') changeCallback = handler;
      }),
      removeEventListener: vi.fn(),
    }));

    setupSystemThemeListener((resolved) => {
      applyThemeToDOM(THEMES.SYSTEM);
    });

    // Initial state: light OS -> no dark class
    applyThemeToDOM(THEMES.SYSTEM);
    expect(document.documentElement.getAttribute('data-theme')).toBe('system');
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    // Simulate OS toggling to dark
    window.matchMedia = vi.fn().mockImplementation((query) => ({
      matches: true, // dark
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));

    if (changeCallback) {
      changeCallback({ matches: true });
    } else {
      applyThemeToDOM(THEMES.SYSTEM);
    }

    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('renders ThemeSwitcher button with accessibility attributes and opens menu on click', async () => {
    render(<ThemeSwitcher showLabel={true} />);

    const button = screen.getByRole('button', { name: /theme selector/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveAttribute('aria-haspopup', 'listbox');
    expect(button).toHaveAttribute('aria-expanded', 'false');

    // Click to open
    fireEvent.click(button);
    expect(button).toHaveAttribute('aria-expanded', 'true');

    // Options should be visible
    expect(screen.getByRole('option', { name: /white/i })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: /black/i })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: /blue/i })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: /system/i })).toBeInTheDocument();
  });

  it('allows selecting a theme from the dropdown menu and updates store', async () => {
    render(<ThemeSwitcher />);

    const button = screen.getByRole('button', { name: /theme selector/i });
    fireEvent.click(button);

    const blueOption = screen.getByRole('option', { name: /blue/i });
    fireEvent.click(blueOption);

    expect(useThemeStore.getState().theme).toBe('blue');
    expect(document.documentElement.getAttribute('data-theme')).toBe('blue');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('mock_interview_theme')).toBe('blue');
  });

  it('supports keyboard navigation: Enter opens, Escape closes, Arrow keys navigate', async () => {
    render(<ThemeSwitcher />);

    const button = screen.getByRole('button', { name: /theme selector/i });

    // Press Enter to open
    fireEvent.keyDown(button, { key: 'Enter' });
    expect(button).toHaveAttribute('aria-expanded', 'true');

    // Press Escape to close
    fireEvent.keyDown(button, { key: 'Escape' });
    expect(button).toHaveAttribute('aria-expanded', 'false');

    // Press ArrowDown on button to open
    fireEvent.keyDown(button, { key: 'ArrowDown' });
    expect(button).toHaveAttribute('aria-expanded', 'true');

    // Arrow keys between options
    const options = screen.getAllByRole('option');
    fireEvent.keyDown(options[0], { key: 'ArrowDown' });
    // Pressing Enter on second option selects it
    fireEvent.keyDown(options[1], { key: 'Enter' });

    expect(useThemeStore.getState().theme).toBe('white');
  });
});
