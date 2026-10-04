import React from 'react';

export default function ProgressBar({
  value = 0,
  max = 100,
  color = 'bg-indigo-600 dark:bg-indigo-500',
  height = 'h-2',
  showLabel = false,
  label,
  valueText,
  className = '',
}) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className={`w-full ${className}`}>
      {(showLabel || label || valueText) && (
        <div className="flex items-center justify-between text-xs mb-1.5 font-medium text-slate-600 dark:text-slate-300">
          <span>{label}</span>
          <span>{valueText ?? `${Math.round(percentage)}%`}</span>
        </div>
      )}
      <div className={`w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden ${height}`}>
        <div
          className={`${color} ${height} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
