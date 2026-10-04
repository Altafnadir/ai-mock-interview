import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, Lock, Mail, Eye, EyeOff, LogIn } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import AuthSplitLayout from '../../components/layout/AuthSplitLayout';
import Button from '../../components/ui/Button';

export default function AdminLoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const res = await authApi.login({ email, password });
      if (res.data.user.role !== 'admin') {
        setError('Access denied: This portal is reserved for administrative accounts.');
        toast.error('Access denied: Candidate account cannot access Admin console.');
        return;
      }

      setAuth(res.data);
      toast.success('Admin authentication verified.');
      navigate('/admin');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Invalid administrative credentials.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoAdminFill = () => {
    setEmail('admin@gims.edu.pk');
    setPassword('AdminSecurePassword123!');
  };

  return (
    <AuthSplitLayout
      title="Admin Portal 🛡️"
      subtitle="Sign in to access system analytics, user management, and AI interview pipelines."
      badge="Admin"
    >
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-900/50 flex items-center justify-center text-rose-600 dark:text-rose-400">
              <Shield className="w-4 h-4 stroke-[2.2]" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Administrative Access
              </h2>
              <p className="text-[11px] text-slate-400">Restricted zone</p>
            </div>
          </div>
          <button
            type="button"
            onClick={handleDemoAdminFill}
            className="text-[11px] text-indigo-600 dark:text-indigo-400 font-medium hover:underline bg-indigo-50 dark:bg-indigo-950/40 px-2 py-1 rounded-md"
          >
            Auto-fill Admin
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 text-rose-600 dark:text-rose-400 text-xs font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Admin Email
            </label>
            <input
              id="adminEmail"
              type="email"
              required
              placeholder="admin@gims.edu.pk"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Master Password
            </label>
            <div className="relative">
              <input
                id="adminPassword"
                type={showPassword ? 'text' : 'password'}
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3.5 py-2.5 pr-10 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full font-semibold shadow-sm mt-2"
            isLoading={isLoading}
            icon={LogIn}
          >
            Authenticate Admin
          </Button>
        </form>

        <p className="mt-6 text-center text-xs text-slate-400">
          <Link to="/login" className="hover:text-slate-600 dark:hover:text-slate-300">
            &larr; Candidate Sign In
          </Link>
        </p>
      </div>
    </AuthSplitLayout>
  );
}
