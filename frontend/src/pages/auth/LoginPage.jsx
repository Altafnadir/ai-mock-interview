import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Mail, Lock, LogIn, Sparkles, KeyRound, ShieldCheck } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';
import Logo from '../../components/common/Logo';

export default function LoginPage() {
  const [loginMode, setLoginMode] = useState('password'); // 'password' | 'otp'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { setAuth } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const handlePasswordSubmit = async (e) => {
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

  const handleRequestOtp = async (e) => {
    e.preventDefault();
    if (!email) {
      setError('Please provide your email address.');
      return;
    }
    setError('');
    setIsLoading(true);

    try {
      const res = await authApi.requestOtpLogin(email);
      setOtpSent(true);
      toast.success(res.data.message || 'Verification code sent to your email!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Could not send verification code.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    if (!otpCode || otpCode.length !== 6) {
      setError('Please enter the 6-digit code sent to your email.');
      return;
    }
    setError('');
    setIsLoading(true);

    try {
      const res = await authApi.verifyOtpLogin({ email, code: otpCode });
      setAuth(res.data);
      toast.success(`Signed in successfully as ${res.data.user.full_name}!`);
      if (res.data.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate(from, { replace: true });
      }
    } catch (err) {
      const msg = err.response?.data?.detail || 'Invalid or expired login code.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoCandidateFill = () => {
    setLoginMode('password');
    setEmail('candidate@gims.edu.pk');
    setPassword('CandidatePassword123!');
  };

  const handleGoogleLoginMock = async () => {
    setIsLoading(true);
    try {
      // Simulate Google OAuth ID token exchange
      const mockGoogleIdToken = 'google_oauth_simulated_token_' + Math.random().toString(36).substring(2, 10);
      const res = await authApi.googleLogin(mockGoogleIdToken);
      setAuth(res.data);
      toast.success(`Google sign-in successful: Welcome ${res.data.user.full_name}!`);
      navigate(from, { replace: true });
    } catch (err) {
      toast.error('Google Sign-In failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full">
        {/* Brand Header */}
        <div className="text-center mb-8 flex flex-col items-center">
          <Logo variant="full" size="lg" to="/" className="mb-2" />
          <h2 className="text-xl font-bold text-white mt-2">Welcome Back</h2>
          <p className="text-xs text-slate-400 mt-1">
            Sign in to continue your mock interview preparation
          </p>
        </div>

        {/* Mode Selector Tabs */}
        <div className="flex bg-slate-900 border border-slate-800 rounded-xl p-1 mb-4">
          <button
            type="button"
            onClick={() => { setLoginMode('password'); setError(''); }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              loginMode === 'password'
                ? 'bg-primary-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Password Sign In
          </button>
          <button
            type="button"
            onClick={() => { setLoginMode('otp'); setError(''); }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              loginMode === 'otp'
                ? 'bg-primary-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Passwordless OTP
          </button>
        </div>

        <Card className="border-slate-800 bg-slate-900/90 shadow-2xl">
          {error && (
            <div className="mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium">
              {error}
            </div>
          )}

          {loginMode === 'password' ? (
            <form onSubmit={handlePasswordSubmit} className="space-y-4">
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
            </form>
          ) : (
            <div className="space-y-4">
              {!otpSent ? (
                <form onSubmit={handleRequestOtp} className="space-y-4">
                  <p className="text-xs text-slate-400">
                    Enter your email to receive a secure 6-digit one-time code. No password required.
                  </p>
                  <Input
                    label="Email Address"
                    id="otpEmail"
                    type="email"
                    icon={Mail}
                    required
                    placeholder="candidate@gims.edu.pk"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    className="w-full font-semibold"
                    isLoading={isLoading}
                    icon={KeyRound}
                  >
                    Send One-Time Code
                  </Button>
                </form>
              ) : (
                <form onSubmit={handleVerifyOtp} className="space-y-4">
                  <div className="text-center p-3 bg-primary-950/50 border border-primary-800/40 rounded-lg">
                    <p className="text-xs text-primary-300 font-medium">Code sent to: {email}</p>
                    <button
                      type="button"
                      onClick={() => setOtpSent(false)}
                      className="text-xs text-primary-400 underline mt-1"
                    >
                      Change email
                    </button>
                  </div>

                  <Input
                    label="6-Digit Verification Code"
                    id="otpCode"
                    type="text"
                    maxLength={6}
                    icon={ShieldCheck}
                    required
                    placeholder="123456"
                    className="text-center tracking-widest text-lg font-mono"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value)}
                  />

                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    className="w-full font-semibold"
                    isLoading={isLoading}
                    icon={LogIn}
                  >
                    Verify & Sign In
                  </Button>
                </form>
              )}
            </div>
          )}

          {/* Social / Google Sign-in */}
          <div className="mt-5 pt-5 border-t border-slate-800">
            <button
              type="button"
              onClick={handleGoogleLoginMock}
              disabled={isLoading}
              className="w-full py-2.5 px-4 rounded-xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 text-white text-xs font-semibold flex items-center justify-center gap-2.5 transition-all shadow-sm"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                />
              </svg>
              Continue with Google
            </button>
          </div>

          {/* Quick Demo Fill Shortcut */}
          <div className="pt-3">
            <button
              type="button"
              onClick={handleDemoCandidateFill}
              className="w-full py-2 px-3 rounded-lg bg-primary-950/60 border border-primary-800/60 hover:bg-primary-900/40 text-primary-300 text-xs font-medium flex items-center justify-center gap-1.5 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Fill Demo Candidate Credentials
            </button>
          </div>

          <div className="mt-6 pt-5 border-t border-slate-800 text-center text-xs text-slate-400">
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
