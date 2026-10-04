import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function CalendarGrid({
  currentDate = new Date(),
  practicedDays = [], // array of day numbers or YYYY-MM-DD strings e.g. [3, 4, 10, 12, 13]
  onMonthChange,
  className = '',
}) {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthName = currentDate.toLocaleString('default', { month: 'long' });

  // Compute days in current month
  const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7; // Monday = 0
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const daysArray = Array.from({ length: daysInMonth }, (_, i) => i + 1);
  const emptyDays = Array.from({ length: firstDayIndex }, (_, i) => i);

  const daysOfWeek = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

  const isPracticed = (day) => {
    return practicedDays.includes(day);
  };

  const isToday = (day) => {
    const today = new Date();
    return today.getDate() === day && today.getMonth() === month && today.getFullYear() === year;
  };

  return (
    <div className={`p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3 px-1">
        <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
          {monthName} {year}
        </span>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => onMonthChange?.(-1)}
            className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
            aria-label="Previous month"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={() => onMonthChange?.(1)}
            className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
            aria-label="Next month"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Weekday labels */}
      <div className="grid grid-cols-7 gap-1 text-center mb-1">
        {daysOfWeek.map((d, i) => (
          <span key={i} className="text-[10px] font-semibold text-slate-400">
            {d}
          </span>
        ))}
      </div>

      {/* Days grid */}
      <div className="grid grid-cols-7 gap-1 text-center">
        {emptyDays.map((_, i) => (
          <div key={`empty-${i}`} className="h-7 w-7" />
        ))}
        {daysArray.map((day) => {
          const practiced = isPracticed(day);
          const today = isToday(day);

          return (
            <div
              key={day}
              className={`h-7 w-7 mx-auto rounded-lg text-xs flex items-center justify-center font-medium transition-all ${
                practiced
                  ? 'bg-indigo-600 text-white font-bold shadow-xs'
                  : today
                  ? 'border border-indigo-500 text-indigo-600 dark:text-indigo-400'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              {day}
            </div>
          );
        })}
      </div>
    </div>
  );
}
