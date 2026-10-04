import React from 'react';
import { getScoreRating } from '../../utils/scoreRating';

export default function StatCard({
  title,
  value,
  delta, // e.g. "+2 this week"
  deltaType = 'positive', // positive | neutral | negative
  score, // numerical score if this is a scored stat
  ratingLabel, // explicit label e.g. "Good", "Excellent"
  icon: Icon,
  className = '',
}) {
  const rating = (score !== undefined && score !== null) ? getScoreRating(score) : null;
  const displayRating = ratingLabel || rating?.label;

  return (
    <div className={`bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 sm:p-5 shadow-sm transition-all hover:shadow-md ${className}`}>
      <div className="flex items-start justify-between">
        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 select-none">
          {title}
        </span>
        {Icon && (
          <div className="p-2 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-2.5 flex items-baseline gap-2">
        <span className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          {value ?? '—'}
        </span>
      </div>

      <div className="mt-3 flex items-center gap-1.5 text-xs">
        {displayRating ? (
          <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-medium ${rating?.badgeClass || 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'}`}>
            <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: rating?.color || '#94A3B8' }} />
            {displayRating}
          </span>
        ) : delta ? (
          <span className={`inline-flex items-center gap-1 font-medium ${
            deltaType === 'positive' ? 'text-emerald-600 dark:text-emerald-400' :
            deltaType === 'negative' ? 'text-rose-600 dark:text-rose-400' :
            'text-slate-500 dark:text-slate-400'
          }`}>
            <span>▲</span> {delta}
          </span>
        ) : null}
      </div>
    </div>
  );
}
