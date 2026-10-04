/**
 * Standardized Score Rating System used across the entire application.
 *
 * Rules:
 *  ≥ 88  -> Excellent
 *  83–87 -> Very Good
 *  70–82 -> Good
 *  55–69 -> Needs Improvement
 *  < 55  -> Needs Practice
 */

export function getScoreRating(score) {
  if (score === null || score === undefined || isNaN(score)) {
    return {
      label: 'Not analyzed yet',
      badgeClass: 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400',
      color: '#94A3B8',
      variant: 'neutral',
    };
  }

  const num = Number(score);

  if (num >= 88) {
    return {
      label: 'Excellent',
      badgeClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/50',
      color: '#10B981',
      variant: 'success',
    };
  }

  if (num >= 83) {
    return {
      label: 'Very Good',
      badgeClass: 'bg-sky-50 text-sky-700 border border-sky-200 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-800/50',
      color: '#0EA5E9',
      variant: 'info',
    };
  }

  if (num >= 70) {
    return {
      label: 'Good',
      badgeClass: 'bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/50',
      color: '#F59E0B',
      variant: 'warning',
    };
  }

  if (num >= 55) {
    return {
      label: 'Needs Improvement',
      badgeClass: 'bg-orange-50 text-orange-700 border border-orange-200 dark:bg-orange-950/40 dark:text-orange-300 dark:border-orange-800/50',
      color: '#F97316',
      variant: 'orange',
    };
  }

  return {
    label: 'Needs Practice',
    badgeClass: 'bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800/50',
    color: '#EF4444',
    variant: 'danger',
  };
}
