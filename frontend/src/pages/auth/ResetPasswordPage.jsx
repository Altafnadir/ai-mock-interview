import React, { useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { Lock, CheckCircle2 } from 'lucide-react';
import { authApi } from '../../api/auth';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Card from '../../components/common/Card';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') || '';
  const navigate = useNavigate();

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    setIsLoading(true);
    try {
      const res = await authApi.resetPassword({
        token,
        new_password: newPassword,
      });

      toast.success(res.data.message || 'Password reset successfully.');
      navigate('/login');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to reset password. Link may be expired.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-white">Create New Password</h2>
          <p className="text-xs text-slate-400 mt-2">
            Enter your new secure password below
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
              label="New Password"
              id="newPassword"
              type="password"
              icon={Lock}
              required
              placeholder="••••••••"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />

            <Input
              label="Confirm New Password"
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
              className="w-full mt-2 font-semibold"
              isLoading={isLoading}
              icon={CheckCircle2}
            >
              Update Password
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center">
            <Link to="/login" className="text-xs text-slate-400 hover:text-slate-200">
              Cancel & Return to Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
