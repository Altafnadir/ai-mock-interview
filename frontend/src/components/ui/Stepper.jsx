import React from 'react';
import { Check } from 'lucide-react';

export default function Stepper({
  steps = [], // [{ id, title, description }]
  currentStep = 0, // 0-indexed
  onStepClick,
  className = '',
}) {
  return (
    <div className={`w-full py-4 ${className}`}>
      <div className="flex items-center justify-between">
        {steps.map((step, idx) => {
          const isCompleted = idx < currentStep;
          const isActive = idx === currentStep;
          const isClickable = onStepClick && idx <= currentStep;

          return (
            <React.Fragment key={step.id || idx}>
              <div
                className={`flex flex-col items-center relative ${
                  isClickable ? 'cursor-pointer' : ''
                }`}
                onClick={() => isClickable && onStepClick(idx)}
              >
                <div
                  className={`w-9 h-9 rounded-full flex items-center justify-center font-semibold text-xs transition-all ${
                    isCompleted
                      ? 'bg-emerald-600 text-white shadow'
                      : isActive
                      ? 'bg-indigo-600 text-white ring-4 ring-indigo-100 dark:ring-indigo-900/50 shadow'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-500 border border-slate-200 dark:border-slate-700'
                  }`}
                >
                  {isCompleted ? <Check className="w-4 h-4 stroke-[3]" /> : idx + 1}
                </div>
                <span
                  className={`mt-2 text-xs font-medium text-center whitespace-nowrap ${
                    isActive
                      ? 'text-indigo-600 dark:text-indigo-400 font-semibold'
                      : isCompleted
                      ? 'text-slate-800 dark:text-slate-200'
                      : 'text-slate-400 dark:text-slate-500'
                  }`}
                >
                  {step.title}
                </span>
              </div>

              {idx < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-3 mb-6 transition-colors ${
                    idx < currentStep ? 'bg-emerald-500' : 'bg-slate-200 dark:bg-slate-800'
                  }`}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
