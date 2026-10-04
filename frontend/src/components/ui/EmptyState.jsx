import React from 'react';
import Button from './Button';

export default function EmptyState({
  icon: Icon,
  title = 'No data available',
  description = 'There are no records to display at this time.',
  actionText,
  onAction,
  className = '',
}) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 ${className}`}>
      {Icon && (
        <div className="p-3.5 rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 mb-4">
          <Icon className="w-8 h-8" />
        </div>
      )}
      <h4 className="text-base font-semibold text-slate-900 dark:text-slate-100">
        {title}
      </h4>
      <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-sm mt-1.5 mb-5">
        {description}
      </p>
      {actionText && onAction && (
        <Button onClick={onAction} variant="primary" size="sm">
          {actionText}
        </Button>
      )}
    </div>
  );
}
