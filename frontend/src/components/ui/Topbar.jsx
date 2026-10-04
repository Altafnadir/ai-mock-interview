import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Bell, User, Settings, LogOut, Shield } from 'lucide-react';
import Avatar from './Avatar';
import Dropdown, { DropdownItem, DropdownDivider } from './Dropdown';
import ThemeSwitcher from '../common/ThemeSwitcher';
import { useAuthStore } from '../../store/authStore';

export default function Topbar({
  title,
  subtitle,
  unreadNotifications = 0,
  className = '',
}) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate(user?.role === 'admin' ? '/admin/login' : '/login');
  };

  const displayName = user?.name || user?.email?.split('@')[0] || 'User';

  return (
    <header className={`h-16 px-4 sm:px-8 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800 flex items-center justify-between sticky top-0 z-20 transition-colors ${className}`}>
      {/* Title / Greeting Area */}
      <div>
        {title ? (
          <div>
            <h1 className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 tracking-tight">
              {title}
            </h1>
            {subtitle && (
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {subtitle}
              </p>
            )}
          </div>
        ) : null}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Theme Switcher */}
        <ThemeSwitcher />

        {/* Notification Bell */}
        <Link
          to="/notifications"
          className="relative p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-slate-800 transition-colors"
          aria-label="View notifications"
        >
          <Bell className="w-5 h-5" />
          {unreadNotifications > 0 && (
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500 ring-2 ring-white dark:ring-slate-900" />
          )}
        </Link>

        {/* User Avatar Dropdown */}
        <Dropdown
          align="right"
          trigger={({ isOpen }) => (
            <button
              type="button"
              className="flex items-center gap-2 p-1 pl-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none"
            >
              <div className="hidden sm:flex flex-col items-end text-right mr-1">
                <span className="text-xs font-semibold text-slate-900 dark:text-slate-100 leading-tight">
                  {displayName}
                </span>
                <span className="text-[10px] text-slate-400 capitalize">
                  {user?.role || 'Candidate'}
                </span>
              </div>
              <Avatar
                name={displayName}
                size="sm"
                src={user?.avatar_url}
              />
            </button>
          )}
        >
          <div className="px-3.5 py-2.5 border-b border-slate-100 dark:border-slate-800">
            <p className="text-xs font-semibold text-slate-900 dark:text-slate-100 truncate">
              {displayName}
            </p>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate">
              {user?.email}
            </p>
          </div>

          <DropdownItem
            icon={User}
            onClick={() => navigate(user?.role === 'admin' ? '/admin' : '/settings')}
          >
            Profile & Account
          </DropdownItem>

          <DropdownItem
            icon={Settings}
            onClick={() => navigate('/settings')}
          >
            Preferences
          </DropdownItem>

          {user?.role === 'admin' && (
            <DropdownItem
              icon={Shield}
              onClick={() => navigate('/admin')}
            >
              Admin Center
            </DropdownItem>
          )}

          <DropdownDivider />

          <DropdownItem
            icon={LogOut}
            danger
            onClick={handleLogout}
          >
            Sign Out
          </DropdownItem>
        </Dropdown>
      </div>
    </header>
  );
}
