import React from 'react';
import { Play, Clock } from 'lucide-react';
import Badge from './Badge';

export default function VideoCard({
  thumbnail,
  title,
  level = 'Beginner',
  duration = '10 min',
  category,
  onClick,
  className = '',
}) {
  return (
    <div
      onClick={onClick}
      className={`group cursor-pointer bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:border-slate-300 dark:hover:border-slate-700 transition-all duration-200 ${className}`}
    >
      {/* Video Thumbnail with Play Overlay */}
      <div className="relative aspect-video w-full bg-slate-900 overflow-hidden">
        {thumbnail ? (
          <img
            src={thumbnail}
            alt={title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-tr from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center">
            <span className="text-xs font-semibold text-slate-400">Mock Interview AI</span>
          </div>
        )}

        {/* Play Icon Circle Overlay */}
        <div className="absolute inset-0 bg-slate-950/20 group-hover:bg-slate-950/40 flex items-center justify-center transition-colors">
          <div className="w-11 h-11 rounded-full bg-white/90 dark:bg-slate-900/90 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
            <Play className="w-5 h-5 fill-current ml-0.5" />
          </div>
        </div>

        {/* Badges on Thumbnail */}
        <div className="absolute bottom-2.5 left-2.5 flex items-center gap-1.5">
          <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-900/80 text-white backdrop-blur-xs flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {duration}
          </span>
        </div>
      </div>

      {/* Info Content */}
      <div className="p-4">
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <Badge
            variant={level === 'Beginner' ? 'success' : level === 'Intermediate' ? 'info' : 'warning'}
            size="sm"
          >
            {level}
          </Badge>
          {category && (
            <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 truncate">
              {category}
            </span>
          )}
        </div>
        <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 line-clamp-2 transition-colors">
          {title}
        </h4>
      </div>
    </div>
  );
}
