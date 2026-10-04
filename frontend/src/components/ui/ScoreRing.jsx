import React from 'react';
import { getScoreRating } from '../../utils/scoreRating';

export default function ScoreRing({
  score,
  size = 120,
  strokeWidth = 10,
  label, // e.g. "Excellent" or custom
  subtitle,
  centerIcon: CenterIcon,
  className = '',
  useScoreColor = false,
}) {
  const rating = getScoreRating(score);
  const validScore = typeof score === 'number' && !isNaN(score) ? Math.max(0, Math.min(100, score)) : null;

  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = validScore !== null ? circumference - (validScore / 100) * circumference : circumference;

  const strokeColor = useScoreColor ? rating.color : '#4F46E5';

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="rotate-[-90deg] transition-all duration-700 ease-out"
        >
          {/* Background track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            className="text-slate-100 dark:text-slate-800"
          />
          {/* Progress bar */}
          {validScore !== null && (
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              stroke={strokeColor}
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              style={{ transition: 'stroke-dashoffset 0.8s ease-in-out' }}
            />
          )}
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-2">
          {CenterIcon ? (
            <CenterIcon className="w-8 h-8 text-indigo-600 dark:text-indigo-400 mb-1" />
          ) : (
            <span className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
              {validScore !== null ? `${Math.round(validScore)}%` : '—'}
            </span>
          )}
          {label !== false && (
            <span
              className="text-xs font-semibold mt-0.5"
              style={{ color: rating.color }}
            >
              {label || rating.label}
            </span>
          )}
        </div>
      </div>
      {subtitle && (
        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-2 text-center">
          {subtitle}
        </span>
      )}
    </div>
  );
}
