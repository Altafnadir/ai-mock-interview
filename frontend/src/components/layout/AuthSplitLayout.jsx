import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../common/Logo';
import ThemeSwitcher from '../common/ThemeSwitcher';

export default function AuthSplitLayout({
  title = 'Welcome Back! 👋',
  subtitle = 'Sign in to continue your interview preparation journey.',
  badge = null,
  children,
}) {
  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row bg-[#F5F7FB] dark:bg-slate-950 font-sans antialiased">
      {/* Left Panel: Deep Navy Hero (#0B1437) with SVG Illustration */}
      <div className="w-full md:w-5/12 lg:w-1/2 bg-[#0B1437] text-white p-8 sm:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden shrink-0">
        {/* Subtle Tech Glow Orbs */}
        <div className="absolute top-1/4 -left-20 w-80 h-80 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-10 right-0 w-96 h-96 bg-blue-500/15 rounded-full blur-3xl pointer-events-none" />

        {/* Top Header / Brand */}
        <div className="relative z-10 flex items-center justify-between">
          <Logo variant="full" size="md" to="/" badge={badge} />
        </div>

        {/* Middle Content & Original Glowing Cyber Shield SVG Illustration */}
        <div className="relative z-10 my-auto py-10 flex flex-col items-center text-center">
          {/* Cyber Shield + Lock SVG */}
          <div className="relative w-56 h-56 sm:w-64 sm:h-64 mb-8 flex items-center justify-center">
            {/* Glowing isometric platform grid */}
            <svg
              viewBox="0 0 240 240"
              className="w-full h-full drop-shadow-[0_10px_35px_rgba(79,70,229,0.45)]"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Isometric Base Grid */}
              <ellipse cx="120" cy="185" rx="85" ry="32" fill="url(#platformGlow)" opacity="0.6" />
              <path
                d="M40 185 L120 155 L200 185 L120 215 Z"
                stroke="#6366F1"
                strokeWidth="1.5"
                strokeOpacity="0.4"
                fill="none"
              />
              <path
                d="M60 185 L120 162 L180 185 L120 208 Z"
                stroke="#818CF8"
                strokeWidth="1.5"
                strokeOpacity="0.6"
                fill="none"
              />

              {/* Holographic Glowing Pedestal */}
              <path
                d="M100 178 L140 178 L145 192 L95 192 Z"
                fill="#4F46E5"
                fillOpacity="0.5"
                stroke="#818CF8"
                strokeWidth="1"
              />

              {/* Futuristic Cyber Shield */}
              <path
                d="M120 40 L175 62 C175 125 120 158 120 158 C120 158 65 125 65 62 L120 40 Z"
                fill="url(#shieldGrad)"
                stroke="#6366F1"
                strokeWidth="2.5"
              />

              {/* Inner Shield Accent */}
              <path
                d="M120 52 L163 70 C163 118 120 145 120 145 C120 145 77 118 77 70 L120 52 Z"
                stroke="#A5B4FC"
                strokeWidth="1.5"
                strokeOpacity="0.7"
                strokeDasharray="4 3"
              />

              {/* Cyber Padlock */}
              <rect x="105" y="98" width="30" height="24" rx="4" fill="#FFFFFF" fillOpacity="0.95" />
              <path
                d="M111 98 V88 C111 83 115 79 120 79 C125 79 129 83 129 88 V98"
                stroke="#FFFFFF"
                strokeWidth="3"
                strokeLinecap="round"
                fill="none"
              />
              <circle cx="120" cy="108" r="2.5" fill="#4F46E5" />
              <path d="M120 110.5 V116" stroke="#4F46E5" strokeWidth="2" strokeLinecap="round" />

              {/* Vertical light beam from base to shield */}
              <line x1="120" y1="158" x2="120" y2="185" stroke="#818CF8" strokeWidth="2" strokeDasharray="3 3" />

              <defs>
                <linearGradient id="shieldGrad" x1="65" y1="40" x2="175" y2="158" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#4338CA" stopOpacity="0.8" />
                  <stop offset="0.5" stopColor="#3730A3" stopOpacity="0.6" />
                  <stop offset="1" stopColor="#1E1B4B" stopOpacity="0.9" />
                </linearGradient>
                <radialGradient id="platformGlow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(120 185) scale(85 32)">
                  <stop stopColor="#4F46E5" stopOpacity="0.6" />
                  <stop offset="1" stopColor="#4F46E5" stopOpacity="0" />
                </radialGradient>
              </defs>
            </svg>
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white mb-3">
            {title}
          </h2>
          <p className="text-sm text-slate-300 max-w-sm leading-relaxed">
            {subtitle}
          </p>
        </div>

        {/* Bottom Attribution */}
        <div className="relative z-10 text-xs text-slate-400 text-center md:text-left">
          © {new Date().getFullYear()} Mock Interview AI · GIMS, PMAS-AAUR
        </div>
      </div>

      {/* Right Panel: Clean Modern Auth Form */}
      <div className="flex-1 flex flex-col justify-between p-6 sm:p-12 lg:p-16 relative">
        <div className="flex justify-end mb-4">
          <ThemeSwitcher />
        </div>

        <div className="w-full max-w-md mx-auto my-auto py-4">
          {children}
        </div>

        <div className="text-center text-xs text-slate-400 dark:text-slate-500 py-2">
          Protected by role-based access & end-to-end encryption.
        </div>
      </div>
    </div>
  );
}
