import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, CheckCircle2 } from 'lucide-react';
import { authApi } from '../../api/auth';
import { toast } from '../../store/toastStore';
import AuthSplitLayout from '../../components/layout/AuthSplitLayout';
import Button from '../../components/ui/Button';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await authApi.forgotPassword(email);
      setSubmitted(true);
      toast.success('Password reset instructions dispatched.');
    } catch (err) {
      toast.error('Could not process request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthSplitLayout
      title="Reset Your Password 🔑"
      subtitle="We'll send you a secure link to reset your account password."
    >
      <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm">
        {submitted ? (
          <div className="text-center py-4 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-6 h-6 stroke-[2.2]" />
            </div>

            <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
              Check Your Inbox
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              If an account exists for <span className="font-semibold text-slate-800 dark:text-slate-200">{email}</span>, a secure password reset link has been dispatched.
            </p>
            <div className="pt-2">
              <Link to="/login">
                <Button variant="primary" size="md" className="w-full font-semibold">
                  Back to Sign In
                </Button>
              </Link>
            </div>
          </div>
        ) : (
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-1">
              Forgot Password
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-6">
              Enter your registered email address and we'll send you recovery instructions.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                />
              </div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full font-semibold shadow-sm"
                isLoading={isLoading}
              >
                Send Reset Link
              </Button>
            </form>

            <p className="mt-6 text-center text-xs text-slate-400">
              <Link to="/login" className="hover:text-slate-600 dark:hover:text-slate-300">
                &larr; Back to sign in
              </Link>
            </p>
          </div>
        )}
      </div>
    </AuthSplitLayout>
  );
}
