import React, { useState, useEffect, useCallback, useRef } from 'react';

const STORAGE_KEY = 'mock_interview_splash_shown';
const BRAND_NAME = 'Mock Interview AI';
const TAGLINE = 'Practice. Analyze. Get Hired.';

/**
 * Check if the user has already viewed the splash screen during this browser session.
 */
export const hasSeenSplash = () => {
  try {
    if (typeof window === 'undefined' || !window.sessionStorage) return false;
    return window.sessionStorage.getItem(STORAGE_KEY) === 'true';
  } catch {
    return false;
  }
};

/**
 * Mark splash screen as completed in sessionStorage.
 */
export const markSplashSeen = () => {
  try {
    if (typeof window !== 'undefined' && window.sessionStorage) {
      window.sessionStorage.setItem(STORAGE_KEY, 'true');
    }
  } catch {
    // Ignore storage errors in restricted/private browsing modes
  }
};

/**
 * Detect direct deep links where the splash screen should never interrupt the user.
 * e.g., /shared/:token, /interview/:id/room, /interview/:id/processing, /reports/:id
 */
export const isDeepLinkRoute = (pathname) => {
  if (!pathname || typeof pathname !== 'string') return false;
  // Shared public report view
  if (pathname.startsWith('/shared/')) return true;
  // Live interview room or real-time processing room
  if (/^\/interview\/[^/]+\/(room|processing)/.test(pathname)) return true;
  // Direct report permalinks
  if (pathname.startsWith('/reports/')) return true;
  return false;
};

export default function SplashScreen({ currentPath, forceShow = false }) {
  // Check if splash should run
  const shouldDisplayInitially = () => {
    if (typeof window === 'undefined') return false;

    // Check URL query parameters for manual overrides/testing
    const search = window.location.search || '';
    if (search.includes('nosplash=1') || search.includes('nosplash=true')) {
      return false;
    }
    if (forceShow || search.includes('splash=1') || search.includes('force_splash=1')) {
      return true;
    }

    const path = currentPath || window.location.pathname || '/';
    if (isDeepLinkRoute(path)) {
      return false;
    }

    return !hasSeenSplash();
  };

  const [isVisible, setIsVisible] = useState(shouldDisplayInitially);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [typedText, setTypedText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showTagline, setShowTagline] = useState(false);
  const [showProgress, setShowProgress] = useState(false);
  const [isReducedMotion, setIsReducedMotion] = useState(false);

  const timersRef = useRef([]);

  const addTimer = (fn, delay) => {
    const id = setTimeout(fn, delay);
    timersRef.current.push(id);
    return id;
  };

  const clearAllTimers = () => {
    timersRef.current.forEach((id) => clearTimeout(id));
    timersRef.current = [];
  };

  const handleSkip = useCallback(() => {
    clearAllTimers();
    markSplashSeen();
    setIsFadingOut(true);
    setTimeout(() => {
      setIsVisible(false);
    }, 250);
  }, []);

  // Preload logo assets immediately
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const img1 = new Image();
      img1.src = '/brand/logo-icon.png';
      const img2 = new Image();
      img2.src = '/brand/logo-icon-dark.png';
    }
  }, []);

  // Keyboard shortcut listener to skip on any key press
  useEffect(() => {
    if (!isVisible || isFadingOut) return;

    const handleKeyDown = (e) => {
      // Ignore modifier keys alone
      if (['Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) return;
      handleSkip();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isVisible, isFadingOut, handleSkip]);

  // Main animation sequence controller
  useEffect(() => {
    if (!isVisible) return;

    // Check prefers-reduced-motion
    const mediaQuery = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');
    const prefersReduced = mediaQuery ? mediaQuery.matches : false;
    setIsReducedMotion(prefersReduced);

    if (prefersReduced) {
      // Accessible instant version: show full text immediately, hold briefly, then fade out
      setTypedText(BRAND_NAME);
      setShowTagline(true);
      setShowProgress(true);

      addTimer(() => {
        setIsFadingOut(true);
      }, 800);

      addTimer(() => {
        markSplashSeen();
        setIsVisible(false);
      }, 1100);

      return () => clearAllTimers();
    }

    // Sequence for standard animation:
    // 0ms - 850ms: Logo blur-to-focus animation (driven by CSS)
    // 850ms: Start typewriter effect for BRAND_NAME
    addTimer(() => {
      setIsTyping(true);
      let currentIdx = 0;
      const typeInterval = setInterval(() => {
        currentIdx++;
        setTypedText(BRAND_NAME.slice(0, currentIdx));

        if (currentIdx >= BRAND_NAME.length) {
          clearInterval(typeInterval);
          setIsTyping(false);

          // Reveal tagline & progress bar right after name finishes
          setShowTagline(true);
          setShowProgress(true);
        }
      }, 48); // 17 chars * ~48ms = ~816ms

      timersRef.current.push(typeInterval);
    }, 850);

    // 2500ms: Begin smooth fade out
    addTimer(() => {
      setIsFadingOut(true);
    }, 2500);

    // 2900ms: Complete and unmount from DOM
    addTimer(() => {
      markSplashSeen();
      setIsVisible(false);
    }, 2900);

    return () => clearAllTimers();
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="Mock Interview AI loading intro"
      onClick={handleSkip}
      className={`fixed inset-0 z-[9999] flex flex-col items-center justify-center select-none overflow-hidden transition-all duration-350 ease-out cursor-pointer ${
        isFadingOut ? 'opacity-0 scale-[0.99] pointer-events-none' : 'opacity-100 scale-100'
      } bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-white`}
    >
      {/* Background ambient lighting effects */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 sm:w-96 sm:h-96 rounded-full blur-3xl pointer-events-none transition-opacity duration-1000 dark:bg-primary-600/15 bg-primary-500/10 animate-splash-pulse-glow"
        aria-hidden="true"
      />
      <div
        className="absolute -top-24 -right-24 w-72 h-72 rounded-full blur-3xl pointer-events-none dark:bg-indigo-600/10 bg-sky-400/10"
        aria-hidden="true"
      />

      {/* Screen Reader Announcement */}
      <span className="sr-only">
        Mock Interview AI - Practice. Analyze. Get Hired. App is loading. Press any key or click Skip to proceed immediately.
      </span>

      {/* Skip Button */}
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          handleSkip();
        }}
        aria-label="Skip splash screen"
        className="absolute top-5 right-5 sm:top-6 sm:right-6 px-3.5 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white bg-white/70 hover:bg-white dark:bg-slate-900/70 dark:hover:bg-slate-800 border border-slate-200/80 dark:border-slate-800/80 rounded-full transition-all duration-150 backdrop-blur-md shadow-sm flex items-center gap-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 cursor-pointer z-50 group"
      >
        <span>Skip</span>
        <span className="text-[10px] text-slate-400 dark:text-slate-500 group-hover:text-slate-600 dark:group-hover:text-slate-300">
          (Esc)
        </span>
      </button>

      {/* Main Centered Brand Showcase */}
      <div className="relative z-10 flex flex-col items-center text-center px-4 max-w-md w-full">
        {/* Animated Brand Logo (Blur-to-focus) */}
        <div className="relative mb-5 flex items-center justify-center">
          <picture className={isReducedMotion ? 'opacity-100' : 'animate-splash-blur-focus'}>
            <source srcSet="/brand/logo-icon-dark.png" media="(prefers-color-scheme: dark)" />
            {/* Light mode icon */}
            <img
              src="/brand/logo-icon.png"
              alt="Mock Interview AI"
              width={104}
              height={104}
              className="w-20 h-20 sm:w-26 sm:h-26 object-contain dark:hidden drop-shadow-md"
              loading="eager"
            />
            {/* Dark mode icon */}
            <img
              src="/brand/logo-icon-dark.png"
              alt="Mock Interview AI"
              width={104}
              height={104}
              className="w-20 h-20 sm:w-26 sm:h-26 object-contain hidden dark:block drop-shadow-[0_0_25px_rgba(24,88,232,0.35)]"
              loading="eager"
            />
          </picture>
        </div>

        {/* Brand Name with Typewriter Effect */}
        <div className="min-h-[2.5rem] sm:min-h-[3rem] flex items-center justify-center">
          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white flex items-center">
            <span>{typedText}</span>
            {isTyping && (
              <span
                className="inline-block w-[2.5px] h-[0.9em] ml-1 bg-primary-600 dark:bg-primary-400 align-middle animate-splash-blink"
                aria-hidden="true"
              />
            )}
          </h1>
        </div>

        {/* Brand Tagline */}
        <div className="min-h-[1.5rem] mt-2">
          {showTagline && (
            <p
              className={`text-xs sm:text-sm font-semibold tracking-wider uppercase text-slate-500 dark:text-slate-400 ${
                isReducedMotion ? 'opacity-100' : 'animate-splash-fade-in-up'
              }`}
            >
              {TAGLINE}
            </p>
          )}
        </div>

        {/* Elegant Progress / Pulse Bar */}
        <div className="mt-7 w-44 sm:w-56 h-1 bg-slate-200 dark:bg-slate-800/80 rounded-full overflow-hidden shadow-inner">
          {showProgress && (
            <div
              className={`h-full bg-gradient-to-r from-primary-600 via-sky-400 to-primary-600 rounded-full ${
                isReducedMotion ? 'w-full' : 'animate-splash-progress'
              }`}
            />
          )}
        </div>
      </div>
    </div>
  );
}
