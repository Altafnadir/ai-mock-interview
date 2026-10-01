import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Loader({ text = 'Loading...', size = 'md', className = '' }) {
  const sizeMap = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <Loader2 className={`${sizeMap[size]} animate-spin text-primary-600 dark:text-primary-400 mb-3`} />
      {text && (
        <p className="text-sm font-medium text-slate-600 dark:text-slate-400 animate-pulse">
          {text}
        </p>
      )}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="glass-card rounded-xl p-5 animate-pulse space-y-4">
      <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/3"></div>
      <div className="space-y-2">
        <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded"></div>
        <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-5/6"></div>
      </div>
      <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-1/4 pt-2"></div>
    </div>
  );
}
