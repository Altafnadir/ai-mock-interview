import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Mail, Lock, LogIn, Sparkles } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { setAuth } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const res = await authApi.login({ email, password });
      setAuth(res.data);
      toast.success(`Welcome back, ${res.data.user.full_name}!`);
      if (res.data.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate(from, { replace: true });
      }
    } catch (err) {
      const msg = err.response?.data?.detail || 'Invalid email or password.';
      setError(msg);
      toast.error(msg);
      if (msg.includes('Email not verified')) {
        navigate('/verify-otp', { state: { email } });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoCandidateFill = () => {
    setEmail('candidate@gims.edu.pk');
    setPassword('CandidatePassword123!');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-block">
            <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-primary-400 to-indigo-300 bg-clip-text text-transparent">
              AI Mock Interview Prep
            </span>
          </Link>
          <h2 className="text-xl font-bold text-white mt-3">Welcome Back</h2>
          <p className="text-xs text-slate-400 mt-1">
            Sign in to continue your mock interview preparation
          </p>
        </div>

        <Card className="border-slate-800 bg-slate-900/90 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium">
                {error}
              </div>
            )}

            <Input
              label="Email Address"
              id="email"
              type="email"
              icon={Mail}
              required
              placeholder="candidate@gims.edu.pk"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Password
                </span>
                <Link
                  to="/forgot-password"
                  className="text-xs text-primary-400 hover:text-primary-300"
                >
                  Forgot password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                icon={Lock}
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full mt-2 font-semibold shadow-md shadow-primary-600/30"
              isLoading={isLoading}
              icon={LogIn}
            >
              Sign In
            </Button>

            {/* Quick Demo Fill Shortcut */}
            <div className="pt-2">
              <button
                type="button"
                onClick={handleDemoCandidateFill}
                className="w-full py-2 px-3 rounded-lg bg-primary-950/60 border border-primary-800/60 hover:bg-primary-900/40 text-primary-300 text-xs font-medium flex items-center justify-center gap-1.5 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                Fill Demo Candidate Credentials
              </button>
            </div>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-xs text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-400 font-semibold hover:text-primary-300">
              Create account
            </Link>
          </div>
        </Card>

        <div className="text-center mt-6">
          <Link to="/admin/login" className="text-xs text-slate-500 hover:text-slate-400">
            Administrator Portal &rarr;
          </Link>
        </div>
      </div>
    </div>
  );
}
