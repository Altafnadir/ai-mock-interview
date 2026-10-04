import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, User, UserPlus } from 'lucide-react';
import { authApi } from '../../api/auth';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';
import Logo from '../../components/common/Logo';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    setIsLoading(true);

    try {
      const res = await authApi.register({
        full_name: fullName,
        email,
        password,
      });

      toast.success(res.data.message || 'Verification code sent to your email.');
      navigate('/verify-otp', { state: { email } });
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full">
        <div className="text-center mb-8 flex flex-col items-center">
          <Logo variant="full" size="lg" to="/" className="mb-2" />
          <h2 className="text-xl font-bold text-white mt-2">Create Candidate Account</h2>
          <p className="text-xs text-slate-400 mt-1">
            Join Mock Interview AI to start your personalized preparation
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
              label="Full Name"
              id="fullName"
              icon={User}
              required
              placeholder="Hamza Ali"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />

            <Input
              label="Email Address"
              id="email"
              type="email"
              icon={Mail}
              required
              placeholder="student@gims.edu.pk"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <Input
              label="Password (min 8 chars)"
              id="password"
              type="password"
              icon={Lock}
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Input
              label="Confirm Password"
              id="confirmPassword"
              type="password"
              icon={Lock}
              required
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full mt-2 font-semibold shadow-md shadow-primary-600/30"
              isLoading={isLoading}
              icon={UserPlus}
            >
              Register & Send OTP
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-xs text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-primary-400 font-semibold hover:text-primary-300">
              Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
