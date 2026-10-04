import React from 'react';

export default function Avatar({
  src,
  alt = '',
  name = '',
  size = 'md', // sm | md | lg | xl
  status, // online | offline | busy
  className = '',
}) {
  const sizes = {
    sm: 'w-7 h-7 text-xs',
    md: 'w-9 h-9 text-sm',
    lg: 'w-12 h-12 text-base font-semibold',
    xl: 'w-16 h-16 text-xl font-bold',
  };

  const getInitials = (n) => {
    if (!n) return 'U';
    const parts = n.trim().split(' ');
    if (parts.length >= 2) return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    return parts[0].slice(0, 2).toUpperCase();
  };

  return (
    <div className={`relative inline-flex items-center justify-center shrink-0 ${sizes[size]} rounded-full select-none ${className}`}>
      {src ? (
        <img
          src={src}
          alt={alt || name}
          className="w-full h-full object-cover rounded-full border border-slate-200 dark:border-slate-700 shadow-sm"
        />
      ) : (
        <div className="w-full h-full rounded-full bg-indigo-600 text-white flex items-center justify-center font-medium shadow-sm">
          {getInitials(name)}
        </div>
      )}
      {status && (
        <span
          className={`absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full ring-2 ring-white dark:ring-slate-900 ${
            status === 'online' ? 'bg-emerald-500' :
            status === 'busy' ? 'bg-rose-500' :
            'bg-slate-400'
          }`}
        />
      )}
    </div>
  );
}
