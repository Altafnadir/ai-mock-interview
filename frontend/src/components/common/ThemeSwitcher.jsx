import React, { useState, useRef, useEffect } from 'react';
import { useThemeStore, THEMES } from '../../store/themeStore';
import { Monitor, Sun, Moon, Palette, Check, ChevronDown } from 'lucide-react';

const THEME_OPTIONS = [
  {
    id: THEMES.SYSTEM,
    label: 'System',
    hint: 'Follows OS preference',
    icon: Monitor,
    badgeColor: 'bg-slate-500/20 text-slate-400',
  },
  {
    id: THEMES.WHITE,
    label: 'White',
    hint: 'Pure clean light',
    icon: Sun,
    badgeColor: 'bg-amber-500/20 text-amber-500',
  },
  {
    id: THEMES.BLACK,
    label: 'Black',
    hint: 'Pure deep dark',
    icon: Moon,
    badgeColor: 'bg-zinc-700/40 text-zinc-300',
  },
  {
    id: THEMES.BLUE,
    label: 'Blue',
    hint: 'Dark navy blue',
    icon: Palette,
    badgeColor: 'bg-blue-500/20 text-blue-400',
  },
];

export default function ThemeSwitcher({
  align = 'right',
  size = 'md',
  showLabel = false,
  className = '',
}) {
  const { theme, setTheme } = useThemeStore();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);
  const triggerRef = useRef(null);
  const optionRefs = useRef([]);

  const currentOption = THEME_OPTIONS.find((t) => t.id === theme) || THEME_OPTIONS[0];
  const CurrentIcon = currentOption.icon;

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('touchstart', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, [isOpen]);

  // Focus management when menu opens
  useEffect(() => {
    if (isOpen) {
      const activeIndex = THEME_OPTIONS.findIndex((t) => t.id === theme);
      const targetIndex = activeIndex >= 0 ? activeIndex : 0;
      setTimeout(() => {
        optionRefs.current[targetIndex]?.focus();
      }, 50);
    }
  }, [isOpen, theme]);

  const handleTriggerKeyDown = (e) => {
    if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setIsOpen(true);
    } else if (e.key === 'Escape' && isOpen) {
      e.preventDefault();
      setIsOpen(false);
    }
  };

  const handleOptionKeyDown = (e, index) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      const nextIndex = (index + 1) % THEME_OPTIONS.length;
      optionRefs.current[nextIndex]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIndex = (index - 1 + THEME_OPTIONS.length) % THEME_OPTIONS.length;
      optionRefs.current[prevIndex]?.focus();
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setTheme(THEME_OPTIONS[index].id);
      setIsOpen(false);
      triggerRef.current?.focus();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setIsOpen(false);
      triggerRef.current?.focus();
    } else if (e.key === 'Tab') {
      setIsOpen(false);
    }
  };

  const handleSelect = (selectedId) => {
    setTheme(selectedId);
    setIsOpen(false);
    triggerRef.current?.focus();
  };

  return (
    <div className={`relative inline-block text-left ${className}`} ref={containerRef}>
      <button
        ref={triggerRef}
        type="button"
        id="theme-switcher-button"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-label={`Theme selector. Current theme: ${currentOption.label}`}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleTriggerKeyDown}
        className={`flex items-center gap-1.5 p-2 rounded-xl border border-slate-200/80 dark:border-slate-800/80 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 shadow-sm ${
          size === 'sm' ? 'text-xs p-1.5' : 'text-sm p-2'
        }`}
        title={`Theme: ${currentOption.label}`}
      >
        <CurrentIcon className={size === 'sm' ? 'w-4 h-4' : 'w-4 h-4 sm:w-4.5 sm:h-4.5'} />
        {showLabel && (
          <span className="text-xs font-semibold">{currentOption.label}</span>
        )}
        <ChevronDown
          className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {isOpen && (
        <div
          role="listbox"
          aria-labelledby="theme-switcher-button"
          tabIndex={-1}
          className={`absolute ${
            align === 'right' ? 'right-0' : 'left-0'
          } mt-2 w-52 sm:w-56 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl shadow-2xl p-1.5 z-50 animate-in fade-in zoom-in-95 duration-150 focus:outline-none`}
        >
          <div className="px-3 py-1.5 border-b border-slate-100 dark:border-slate-800/80 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              Appearance Theme
            </span>
          </div>

          <div className="space-y-0.5">
            {THEME_OPTIONS.map((opt, index) => {
              const Icon = opt.icon;
              const isSelected = theme === opt.id;
              return (
                <button
                  key={opt.id}
                  ref={(el) => (optionRefs.current[index] = el)}
                  role="option"
                  aria-selected={isSelected}
                  tabIndex={0}
                  type="button"
                  onClick={() => handleSelect(opt.id)}
                  onKeyDown={(e) => handleOptionKeyDown(e, index)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all text-left focus:outline-none focus:ring-1 focus:ring-primary-500 ${
                    isSelected
                      ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400 font-semibold'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/70 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <span
                      className={`p-1.5 rounded-lg ${opt.badgeColor} flex items-center justify-center`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                    </span>
                    <div>
                      <div className="leading-snug">{opt.label}</div>
                      <div className="text-[10px] text-slate-400 dark:text-slate-500 leading-tight">
                        {opt.hint}
                      </div>
                    </div>
                  </div>
                  {isSelected && (
                    <Check className="w-4 h-4 text-primary-500 flex-shrink-0" />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
