import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  Video,
  History,
  BookOpen,
  Sparkles,
  User,
  Bell,
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Start Interview', path: '/interview/setup', icon: Video, highlight: true },
  { name: 'Resume Manager', path: '/resume', icon: FileText },
  { name: 'Session History', path: '/history', icon: History },
  { name: 'Learning Resources', path: '/resources', icon: BookOpen },
  { name: 'Practice Drills', path: '/practice', icon: Sparkles },
  { name: 'My Profile', path: '/profile', icon: User },
  { name: 'Notifications', path: '/notifications', icon: Bell },
];

export default function CandidateSidebar() {
  return (
    <aside className="w-64 flex-shrink-0 hidden md:block border-r border-slate-200/80 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm min-h-[calc(100vh-4rem)] p-4">
      <div className="space-y-1">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-primary-600 text-white shadow-sm shadow-primary-500/20 font-semibold'
                    : item.highlight
                    ? 'text-primary-600 dark:text-primary-400 bg-primary-50/80 dark:bg-primary-950/40 hover:bg-primary-100 dark:hover:bg-primary-900/60 font-semibold'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </div>

      {/* University & Project Badge */}
      <div className="mt-8 p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 text-xs text-slate-500 dark:text-slate-400">
        <p className="font-semibold text-slate-700 dark:text-slate-300">PMAS-AAUR (GIMS)</p>
        <p className="text-[11px] mt-0.5">Final Year Project 2024-2026</p>
        <div className="mt-2 text-[10px] text-primary-600 dark:text-primary-400 font-mono font-medium">
          GIMS-BSSE-F202206
        </div>
      </div>
    </aside>
  );
}
