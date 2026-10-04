import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  HelpCircle,
  FolderTree,
  BookOpen,
  Video,
  FileCheck2,
  BarChart3,
  BellRing,
  Activity,
  ShieldAlert,
} from 'lucide-react';

const ADMIN_NAV = [
  { name: 'Dashboard', path: '/admin', icon: LayoutDashboard },
  { name: 'User Management', path: '/admin/users', icon: Users },
  { name: 'Question Bank', path: '/admin/questions', icon: HelpCircle },
  { name: 'Taxonomy & Content', path: '/admin/content', icon: FolderTree },
  { name: 'Learning Resources', path: '/admin/resources', icon: BookOpen },
  { name: 'Session Inspector', path: '/admin/sessions', icon: Video },
  { name: 'Reports Archive', path: '/admin/reports', icon: FileCheck2 },
  { name: 'Analytics & KPIs', path: '/admin/analytics', icon: BarChart3 },
  { name: 'Announcements', path: '/admin/notifications', icon: BellRing },
  { name: 'System Monitoring', path: '/admin/monitoring', icon: Activity },
  { name: 'Security & Backup', path: '/admin/security', icon: ShieldAlert },
];

export default function AdminSidebar() {
  return (
    <aside className="w-64 flex-shrink-0 hidden md:block border-r border-slate-200/80 dark:border-slate-800/80 bg-white/90 dark:bg-slate-900/90 text-slate-800 dark:text-slate-200 min-h-[calc(100vh-4rem)] p-4">
      <div className="mb-4 px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 text-xs font-semibold flex items-center gap-2">
        <ShieldAlert className="w-4 h-4" />
        ADMINISTRATION CONSOLE
      </div>

      <div className="space-y-1">
        {ADMIN_NAV.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/admin'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-amber-600 text-white shadow-sm font-semibold'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
}
