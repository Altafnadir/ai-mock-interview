import React from 'react';
import { Link } from 'react-router-dom';

/**
 * Reusable brand Logo component supporting light/dark variants,
 * icon-only, full horizontal, and stacked layouts.
 */
export default function Logo({
  variant = 'full', // 'full' | 'icon' | 'stacked'
  size = 'md',     // 'sm' | 'md' | 'lg' | 'xl'
  badge = null,    // e.g. 'Admin'
  to = '/',
  className = '',
  responsive = false, // If true, icon on small screens, full on md+
}) {
  // Dimensions map
  const dimensions = {
    icon: {
      sm: { w: 28, h: 28, imgClass: 'w-7 h-7' },
      md: { w: 36, h: 36, imgClass: 'w-9 h-9' },
      lg: { w: 48, h: 48, imgClass: 'w-12 h-12' },
      xl: { w: 64, h: 64, imgClass: 'w-16 h-16' },
    },
    full: {
      sm: { w: 140, h: 32, imgClass: 'h-8 w-auto' },
      md: { w: 175, h: 40, imgClass: 'h-10 w-auto' },
      lg: { w: 220, h: 50, imgClass: 'h-12 w-auto' },
      xl: { w: 280, h: 64, imgClass: 'h-16 w-auto' },
    },
    stacked: {
      sm: { w: 80, h: 80, imgClass: 'w-20 h-20' },
      md: { w: 120, h: 120, imgClass: 'w-30 h-30' },
      lg: { w: 160, h: 160, imgClass: 'w-40 h-40' },
      xl: { w: 200, h: 200, imgClass: 'w-48 h-48' },
    }
  };

  const dim = dimensions[variant]?.[size] || dimensions.full.md;

  const content = (
    <div className={`inline-flex items-center gap-2 select-none group ${className}`}>
      {/* Responsive behavior: show icon on mobile, full on md+ */}
      {responsive ? (
        <>
          <div className="block md:hidden">
            <picture>
              <source srcSet="/brand/logo-icon-dark.png" media="(prefers-color-scheme: dark)" />
              <img
                src="/brand/logo-icon.png"
                alt="Mock Interview AI"
                width={36}
                height={36}
                className="w-9 h-9 object-contain dark:hidden"
                loading="eager"
              />
              <img
                src="/brand/logo-icon-dark.png"
                alt="Mock Interview AI"
                width={36}
                height={36}
                className="w-9 h-9 object-contain hidden dark:block"
                loading="eager"
              />
            </picture>
          </div>
          <div className="hidden md:block">
            <picture>
              <source srcSet="/brand/logo-full-dark.png" media="(prefers-color-scheme: dark)" />
              <img
                src="/brand/logo-full.png"
                alt="Mock Interview AI"
                width={dim.w}
                height={dim.h}
                className={`${dim.imgClass} object-contain dark:hidden`}
                loading="eager"
              />
              <img
                src="/brand/logo-full-dark.png"
                alt="Mock Interview AI"
                width={dim.w}
                height={dim.h}
                className={`${dim.imgClass} object-contain hidden dark:block`}
                loading="eager"
              />
            </picture>
          </div>
        </>
      ) : variant === 'icon' ? (
        <picture>
          <img
            src="/brand/logo-icon.png"
            alt="Mock Interview AI"
            width={dim.w}
            height={dim.h}
            className={`${dim.imgClass} object-contain dark:hidden`}
            loading="eager"
          />
          <img
            src="/brand/logo-icon-dark.png"
            alt="Mock Interview AI"
            width={dim.w}
            height={dim.h}
            className={`${dim.imgClass} object-contain hidden dark:block`}
            loading="eager"
          />
        </picture>
      ) : variant === 'stacked' ? (
        <picture>
          <img
            src="/brand/logo-stacked.png"
            alt="Mock Interview AI"
            width={dim.w}
            height={dim.h}
            className={`${dim.imgClass} object-contain`}
            loading="eager"
          />
        </picture>
      ) : (
        <picture>
          <img
            src="/brand/logo-full.png"
            alt="Mock Interview AI"
            width={dim.w}
            height={dim.h}
            className={`${dim.imgClass} object-contain dark:hidden`}
            loading="eager"
          />
          <img
            src="/brand/logo-full-dark.png"
            alt="Mock Interview AI"
            width={dim.w}
            height={dim.h}
            className={`${dim.imgClass} object-contain hidden dark:block`}
            loading="eager"
          />
        </picture>
      )}

      {badge && (
        <span className="ml-1.5 px-2 py-0.5 text-[11px] font-bold uppercase tracking-wider rounded-md bg-primary-500/10 text-primary-600 dark:text-primary-400 border border-primary-500/20">
          {badge}
        </span>
      )}
    </div>
  );

  if (to) {
    return (
      <Link to={to} className="inline-flex items-center focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-lg">
        {content}
      </Link>
    );
  }

  return content;
}
