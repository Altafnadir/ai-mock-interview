import React, { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { KeyRound, ArrowRight, RotateCw } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import Logo from '../../components/common/Logo';

export default function OTPVerificationPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();

  const [email, setEmail] = useState(location.state?.email || '');
  const [digits, setDigits] = useState(['', '', '', '', '', '']);
  const [isLoading, setIsLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [countdown, setCountdown] = useState(60);
  const [error, setError] = useState('');

  const inputRefs = useRef([]);

  useEffect(() => {
    if (inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, []);

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const handleDigitChange = (index, value) => {
    if (!/^\d*$/.test(value)) return;
    const newDigits = [...digits];
    newDigits[index] = value.slice(-1);
    setDigits(newDigits);

    if (value && index < 5 && inputRefs.current[index + 1]) {
      inputRefs.current[index + 1].focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0 && inputRefs.current[index - 1]) {
      inputRefs.current[index - 1].focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').trim().slice(0, 6);
    if (/^\d+$/.test(pasted)) {
      const newDigits = [...digits];
      for (let i = 0; i < pasted.length; i++) {
        newDigits[i] = pasted[i];
      }
      setDigits(newDigits);
      if (inputRefs.current[Math.min(pasted.length, 5)]) {
        inputRefs.current[Math.min(pasted.length, 5)].focus();
      }
    }
  };

  const handleVerify = async (e) => {
    if (e) e.preventDefault();
    setError('');
    const code = digits.join('');
    if (code.length !== 6) {
      setError('Please enter all 6 digits of your verification code.');
      return;
    }

    setIsLoading(true);
    try {
      const res = await authApi.verifyOtp({
        email,
        code,
        purpose: 'register',
      });

      setAuth(res.data);
      toast.success('Account verified successfully! Welcome to your dashboard.');
      navigate('/dashboard');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Verification failed. Please check the code.';
      setError(msg);
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResend = async () => {
    if (countdown > 0 || resending) return;
    setResending(true);
    setError('');
    try {
      const res = await authApi.resendOtp({ email, purpose: 'register' });
      toast.success(res.data.message || 'Verification code resent.');
      setCountdown(60);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to resend code.');
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full">
        <div className="text-center mb-8 flex flex-col items-center">
          <Logo variant="full" size="md" to="/" className="mb-4" />
          <h2 className="text-2xl font-bold text-white">Verify Your Email</h2>
          <p className="text-xs text-slate-400 mt-2">
            Enter the 6-digit verification code dispatched to:
          </p>
          <div className="mt-1 font-semibold text-primary-400 text-sm">{email || 'your email'}</div>
        </div>

        <Card className="border-slate-800 bg-slate-900/90 shadow-2xl">
          <form onSubmit={handleVerify} className="space-y-6">
            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium text-center">
                {error}
              </div>
            )}

            {/* 6 Digit Input Boxes */}
            <div className="flex justify-between gap-2" onPaste={handlePaste}>
              {digits.map((digit, idx) => (
                <input
                  key={idx}
                  ref={(el) => (inputRefs.current[idx] = el)}
                  type="text"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleDigitChange(idx, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(idx, e)}
                  className="w-12 h-14 text-center text-xl font-bold rounded-xl bg-slate-950 border border-slate-700 text-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all"
                />
              ))}
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full font-semibold shadow-md shadow-primary-600/30"
              isLoading={isLoading}
              icon={ArrowRight}
            >
              Verify & Enter Dashboard
            </Button>
          </form>

          {/* Resend Section */}
          <div className="mt-6 pt-6 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Didn't receive the code?</span>
            <button
              type="button"
              disabled={countdown > 0 || resending}
              onClick={handleResend}
              className="font-semibold text-primary-400 hover:text-primary-300 disabled:opacity-50 flex items-center gap-1"
            >
              <RotateCw className={`w-3.5 h-3.5 ${resending ? 'animate-spin' : ''}`} />
              {countdown > 0 ? `Resend in ${countdown}s` : 'Resend Code'}
            </button>
          </div>
        </Card>

        <div className="text-center mt-6">
          <Link to="/login" className="text-xs text-slate-500 hover:text-slate-400">
            &larr; Back to Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
