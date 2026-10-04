import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, Lock, Mail, ArrowRight, Sparkles } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';
import Logo from '../../components/common/Logo';
import ThemeSwitcher from '../../components/common/ThemeSwitcher';

export default function AdminLoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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
    <div className="min-h-screen relative flex items-center justify-center p-4 bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      {/* Top Right Theme Switcher */}
      <div className="absolute top-4 right-4 z-20">
        <ThemeSwitcher />
      </div>

      <div className="max-w-md w-full">
        <div className="text-center mb-8 flex flex-col items-center">
          <Logo variant="full" size="lg" to="/" badge="Admin" className="mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">System Administration</h2>
          <p className="text-xs text-amber-600 dark:text-amber-400 font-medium uppercase tracking-wider mt-1">
            Authorized Personnel Only
          </p>
        </div>

        <Card className="border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/90 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium">
                {error}
              </div>
            )}

            <Input
              label="Admin Email"
              id="adminEmail"
              type="email"
              icon={Mail}
              required
              placeholder="admin@gims.edu.pk"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <Input
              label="Admin Password"
              id="adminPassword"
              type="password"
              icon={Lock}
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
              size="lg"
              className="w-full mt-2 font-semibold bg-amber-600 hover:bg-amber-700 text-white focus:ring-amber-500 shadow-md shadow-amber-600/30"
              isLoading={isLoading}
              icon={ArrowRight}
            >
              Authenticate Admin
            </Button>

            {/* Quick Fill Admin Button */}
            <div className="pt-2">
              <button
                type="button"
                onClick={handleDemoAdminFill}
                className="w-full py-2 px-3 rounded-lg bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-medium flex items-center justify-center gap-1.5 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                Fill Seeded Admin Credentials
              </button>
            </div>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-800 text-center text-xs text-slate-500 dark:text-slate-400">
            Candidate looking for interview practice?{' '}
            <Link to="/login" className="text-primary-600 dark:text-primary-400 hover:text-primary-500 font-medium">
              Candidate Login &rarr;
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
