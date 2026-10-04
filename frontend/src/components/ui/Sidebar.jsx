import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  Video,
  Bot,
  History,
  BarChart3,
  BookOpen,
  Award,
  Settings,
  LogOut,
  Users,
  HelpCircle,
  FolderKanban,
  ShieldCheck,
  Activity,
  Layers,
} from 'lucide-react';
import Logo from '../common/Logo';
import { useAuthStore } from '../../store/authStore';

export const candidateNavItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/resume', label: 'Resume Analysis', icon: FileText },
  { to: '/interview/setup', label: 'Mock Interview', icon: Video },
  { to: '/coach', label: 'AI Coach', icon: Bot },
  { to: '/history', label: 'Interview History', icon: History },
  { to: '/reports', label: 'Reports', icon: BarChart3 },
  { to: '/learning', label: 'Learning Center', icon: BookOpen },
  { to: '/achievements', label: 'Achievements', icon: Award },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export const adminNavItems = [
  { to: '/admin', label: 'Overview', icon: LayoutDashboard },
  { to: '/admin/users', label: 'Users', icon: Users },
  { to: '/admin/sessions', label: 'Interviews', icon: Video },
  { to: '/admin/reports', label: 'Reports', icon: BarChart3 },
  { to: '/admin/questions', label: 'Question Bank', icon: HelpCircle },
  { to: '/admin/resources', label: 'Resources', icon: BookOpen },
  { to: '/admin/analytics', label: 'Analytics', icon: Activity },
  { to: '/admin/content', label: 'Taxonomy', icon: Layers },
  { to: '/admin/monitoring', label: 'System Monitoring', icon: FolderKanban },
  { to: '/admin/security', label: 'Settings & Security', icon: ShieldCheck },
];

export default function Sidebar({
  role = 'candidate',
  className = '',
}) {
  const { logout, user } = useAuthStore();
  const navigate = useNavigate();
  const items = role === 'admin' ? adminNavItems : candidateNavItems;

  const handleLogout = () => {
    logout();
    navigate(role === 'admin' ? '/admin/login' : '/login');
  };

  return (
    <aside
      className={`w-60 shrink-0 bg-white dark:bg-slate-900 border-r border-slate-200/80 dark:border-slate-800 flex flex-col justify-between h-screen sticky top-0 z-30 ${className}`}
    >
      {/* Top Brand Header */}
      <div className="p-5 border-b border-slate-100 dark:border-slate-800/80 flex items-center justify-between">
        <Logo showText={true} size="md" />
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto no-scrollbar">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/dashboard' || item.to === '/admin'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 font-semibold shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0 stroke-[2.2]" />
              <span className="truncate">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom Profile / Logout Footer */}
      <div className="p-3 border-t border-slate-100 dark:border-slate-800">
        <button
          type="button"
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors"
        >
          <LogOut className="w-4 h-4 shrink-0" />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
