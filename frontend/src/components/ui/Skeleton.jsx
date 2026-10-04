import React from 'react';

export default function Skeleton({
  variant = 'text', // text | circular | rectangular | card
  width,
  height,
  className = '',
}) {
  const base = 'animate-pulse bg-slate-200 dark:bg-slate-800 rounded-lg';

  if (variant === 'circular') {
    return (
      <div
        className={`${base} rounded-full shrink-0 ${className}`}
        style={{ width: width || 40, height: height || 40 }}
      />
    );
  }

  if (variant === 'card') {
    return (
      <div className={`p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 ${className}`}>
        <div className="h-4 w-24 bg-slate-200 dark:bg-slate-800 rounded animate-pulse mb-3" />
        <div className="h-8 w-16 bg-slate-200 dark:bg-slate-800 rounded animate-pulse mb-2" />
        <div className="h-4 w-32 bg-slate-200 dark:bg-slate-800 rounded animate-pulse" />
      </div>
    );
  }

  return (
    <div
      className={`${base} ${className}`}
      style={{
        width: width || '100%',
        height: height || (variant === 'text' ? '1rem' : '100%'),
      }}
    />
  );
}
