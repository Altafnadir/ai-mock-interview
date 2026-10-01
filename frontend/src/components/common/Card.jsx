import React from 'react';

export default function Card({
  children,
  title,
  subtitle,
  action,
  className = '',
  bodyClassName = '',
  hoverEffect = false,
  ...props
}) {
  return (
    <div
      className={`glass-card rounded-xl overflow-hidden transition-all duration-200 ${
        hoverEffect ? 'glass-card-hover' : ''
      } ${className}`}
      {...props}
    >
      {(title || subtitle || action) && (
        <div className="px-5 py-4 border-b border-slate-200/80 dark:border-slate-800/80 flex items-center justify-between">
          <div>
            {title && (
              <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                {subtitle}
              </p>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      <div className={`p-5 ${bodyClassName}`}>{children}</div>
    </div>
  );
}
