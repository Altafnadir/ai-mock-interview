import { create } from 'zustand';

export const THEMES = {
  SYSTEM: 'system',
  WHITE: 'white',
  BLACK: 'black',
  BLUE: 'blue',
};

const VALID_THEMES = ['system', 'white', 'black', 'blue'];

export const THEME_META_COLORS = {
  white: '#FFFFFF',
  black: '#000000',
  blue: '#0B1B3F',
};

export function getSystemPreference() {
  if (typeof window === 'undefined' || !window.matchMedia) return 'black';
  try {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'black' : 'white';
  } catch (e) {
    return 'black';
  }
}

export function resolveEffectiveTheme(theme) {
  if (theme === 'system') {
    return getSystemPreference();
  }
  return theme;
}

export function applyThemeToDOM(theme) {
  if (typeof document === 'undefined') return;

  const validTheme = VALID_THEMES.includes(theme) ? theme : 'system';
  const resolved = resolveEffectiveTheme(validTheme);
  const root = document.documentElement;

  // Set data-theme attribute on <html>
  root.setAttribute('data-theme', validTheme);

  // Black and Blue keep class="dark"; White removes class="dark"; System follows OS
  const isDark = resolved === 'black' || resolved === 'blue';
  if (isDark) {
    root.classList.add('dark');
  } else {
    root.classList.remove('dark');
  }

  // Update color-scheme
  root.style.colorScheme = isDark ? 'dark' : 'light';

  // Update <meta name="theme-color">
  const color = resolved === 'white' 
    ? THEME_META_COLORS.white 
    : (resolved === 'blue' ? THEME_META_COLORS.blue : THEME_META_COLORS.black);

  let metaThemeColor = document.querySelector('meta[name="theme-color"]');
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', color);
  } else {
    metaThemeColor = document.createElement('meta');
    metaThemeColor.name = 'theme-color';
    metaThemeColor.content = color;
    document.head.appendChild(metaThemeColor);
  }
}

export function getInitialTheme() {
  try {
    const stored = localStorage.getItem('mock_interview_theme');
    if (stored && VALID_THEMES.includes(stored)) {
      return stored;
    }
    // Backward compatibility check with legacy 'theme' key
    const legacy = localStorage.getItem('theme');
    if (legacy === 'dark') return 'system';
    if (legacy === 'light') return 'white';
  } catch (e) {
    // Safe fallback on localStorage access error
  }
  return 'system';
}

let mqlListener = null;

export function setupSystemThemeListener(callback) {
  if (typeof window === 'undefined' || !window.matchMedia) return () => {};
  try {
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => {
      callback(e.matches ? 'black' : 'white');
    };
    if (mql.addEventListener) {
      mql.addEventListener('change', handler);
      return () => mql.removeEventListener('change', handler);
    } else if (mql.addListener) {
      mql.addListener(handler);
      return () => mql.removeListener(handler);
    }
  } catch (e) {
    // matchMedia not supported or mocked
  }
  return () => {};
}

const initial = getInitialTheme();
if (typeof document !== 'undefined') {
  applyThemeToDOM(initial);
}

export const useThemeStore = create((set, get) => {
  // Setup matchMedia listener for dynamic system OS theme updates
  setupSystemThemeListener(() => {
    if (get().theme === 'system') {
      applyThemeToDOM('system');
      set({ resolvedTheme: resolveEffectiveTheme('system') });
    }
  });

  return {
    theme: initial,
    resolvedTheme: resolveEffectiveTheme(initial),

    setTheme: (newTheme) => {
      const safeTheme = VALID_THEMES.includes(newTheme) ? newTheme : 'system';
      try {
        localStorage.setItem('mock_interview_theme', safeTheme);
        localStorage.setItem('theme', safeTheme);
      } catch (e) {
        // Safe fallback
      }
      applyThemeToDOM(safeTheme);
      set({
        theme: safeTheme,
        resolvedTheme: resolveEffectiveTheme(safeTheme),
      });
    },

    toggleTheme: () => {
      const current = get().theme;
      const next = current === 'white' ? 'black' : 'white';
      get().setTheme(next);
    },
  };
});
