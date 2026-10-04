import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Video,
  BarChart3,
  History,
  MoreHorizontal,
} from 'lucide-react';

export default function MobileBottomNav({ className = '' }) {
  const items = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/interview/setup', label: 'Interview', icon: Video },
    { to: '/reports', label: 'Results', icon: BarChart3 },
    { to: '/history', label: 'History', icon: History },
    { to: '/settings', label: 'More', icon: MoreHorizontal },
  ];

  return (
    <nav className={`sm:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200/80 dark:border-slate-800 px-3 py-2 flex items-center justify-around ${className}`}>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/dashboard'}
            className={({ isActive }) =>
              `flex flex-col items-center gap-1 py-1 px-2.5 rounded-xl text-[10px] font-medium transition-colors ${
                isActive
                  ? 'text-indigo-600 dark:text-indigo-400 font-semibold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900'
              }`
            }
          >
            <Icon className="w-5 h-5 stroke-[2.2]" />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}
