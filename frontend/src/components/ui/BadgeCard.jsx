import React from 'react';
import { Lock, Award } from 'lucide-react';
import ProgressBar from './ProgressBar';

export default function BadgeCard({
  title,
  description,
  points = 50,
  icon: Icon = Award,
  isUnlocked = false,
  earnedAt,
  progress = null, // { current, total }
  className = '',
}) {
  return (
    <div
      className={`p-4 sm:p-5 rounded-2xl border transition-all duration-200 flex flex-col justify-between ${
        isUnlocked
          ? 'bg-white dark:bg-slate-900 border-slate-200/80 dark:border-slate-800 shadow-sm hover:shadow-md'
          : 'bg-slate-50/70 dark:bg-slate-900/40 border-slate-200/60 dark:border-slate-800/60 opacity-80'
      } ${className}`}
    >
      <div>
        {/* Top Icon & Points */}
        <div className="flex items-start justify-between mb-3">
          <div
            className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-xs ${
              isUnlocked
                ? 'bg-gradient-to-tr from-indigo-600 to-indigo-500 text-white shadow-indigo-200 dark:shadow-none'
                : 'bg-slate-200 dark:bg-slate-800 text-slate-400'
            }`}
          >
            {isUnlocked ? <Icon className="w-6 h-6 stroke-[2.2]" /> : <Lock className="w-5 h-5" />}
          </div>
          <span
            className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
              isUnlocked
                ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300 border border-amber-200 dark:border-amber-800/50'
                : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
            }`}
          >
            +{points} pts
          </span>
        </div>

        {/* Title & Description */}
        <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
          {title}
        </h4>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
          {description}
        </p>
      </div>

      {/* Bottom Progress or Earned Date */}
      <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/80 text-[11px]">
        {isUnlocked ? (
          <span className="text-emerald-600 dark:text-emerald-400 font-medium">
            ✓ Earned {earnedAt ? new Date(earnedAt).toLocaleDateString() : 'Recently'}
          </span>
        ) : progress ? (
          <div>
            <div className="flex justify-between text-slate-500 mb-1">
              <span>Progress</span>
              <span>{progress.current} / {progress.total}</span>
            </div>
            <ProgressBar value={progress.current} max={progress.total} height="h-1.5" />
          </div>
        ) : (
          <span className="text-slate-400">Locked</span>
        )}
      </div>
    </div>
  );
}
