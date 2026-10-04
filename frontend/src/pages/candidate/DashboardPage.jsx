import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Sparkles,
  Flame,
  ArrowRight,
  TrendingUp,
  FileText,
  Video,
  Award,
  Calendar,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Area,
} from 'recharts';
import { dashboardApi } from '../../api/dashboard';
import { useAuthStore } from '../../store/authStore';
import { getScoreLabel, getScoreBadgeVariant } from '../../utils/scoreRating';
import StatCard from '../../components/ui/StatCard';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import ProgressBar from '../../components/ui/ProgressBar';
import EmptyState from '../../components/ui/EmptyState';
import Skeleton from '../../components/ui/Skeleton';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [performanceData, setPerformanceData] = useState([]);
  const [timeRange, setTimeRange] = useState('week'); // 'week' | 'month'
  const [isLoading, setIsLoading] = useState(true);

  // Compute time-of-day aware greeting
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const firstName = user?.full_name?.split(' ')[0] || user?.name?.split(' ')[0] || 'Candidate';

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    loadPerformanceSeries(timeRange);
  }, [timeRange]);

  const loadDashboard = async () => {
    try {
      setIsLoading(true);
      const res = await dashboardApi.getOverview();
      setData(res.data);
    } catch (err) {
      console.error('Failed to load dashboard overview:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadPerformanceSeries = async (range) => {
    try {
      const res = await dashboardApi.getPerformance(range);
      if (res.data?.data) {
        setPerformanceData(res.data.data);
      }
    } catch (err) {
      console.error('Failed to load performance chart:', err);
    }
  };

  const metrics = data?.metrics || {};
  const recentSessions = data?.recent_sessions || [];
  const recommendation = data?.ai_recommendation || {
    title: 'Focus Area',
    text: 'Focus on improving your eye contact and reducing filler words. Practice more behavioral questions.',
    action_text: 'Start Recommended Practice',
  };

  // Safe formatting helpers (No hardcoded fake numbers)
  const formatScore = (val) => (val !== undefined && val !== null && val > 0 ? `${Math.round(val)}%` : '—');
  const formatLabel = (val) => (val !== undefined && val !== null && val > 0 ? getScoreLabel(val) : 'Not analyzed');

  if (isLoading && !data) {
    return (
      <div className="space-y-6">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-48" />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[...Array(6)].map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-2xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <Skeleton className="lg:col-span-8 h-80 rounded-2xl" />
          <Skeleton className="lg:col-span-4 h-80 rounded-2xl" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 1. Header Greeting (Time-of-day aware) */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {getGreeting()}, {firstName} 👋
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Ready for today's interview practice?
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/interview/setup">
            <Button variant="primary" size="md" icon={Video} className="shadow-xs font-semibold">
              Practice Now
            </Button>
          </Link>
        </div>
      </div>

      {/* 2. Six Stat Cards Grid (Matching 03_dashboard.png) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        {/* Total Interviews */}
        <StatCard
          title="Total Interviews"
          value={metrics.total_interviews ?? 0}
          delta={metrics.interviews_delta_week !== undefined ? `+${metrics.interviews_delta_week} this week` : null}
          deltaType="positive"
        />

        {/* Average Score */}
        <StatCard
          title="Average Score"
          value={formatScore(metrics.average_score)}
          delta={metrics.score_delta_week ? `+${Math.round(metrics.score_delta_week)}% this week` : null}
          deltaType="positive"
        />

        {/* Confidence */}
        <StatCard
          title="Confidence"
          value={formatScore(metrics.confidence_score)}
          pillLabel={metrics.confidence_score ? getScoreLabel(metrics.confidence_score) : null}
          pillVariant={getScoreBadgeVariant(metrics.confidence_score)}
        />

        {/* Communication */}
        <StatCard
          title="Communication"
          value={formatScore(metrics.communication_score)}
          pillLabel={metrics.communication_score ? getScoreLabel(metrics.communication_score) : null}
          pillVariant={getScoreBadgeVariant(metrics.communication_score)}
        />

        {/* Grammar */}
        <StatCard
          title="Grammar"
          value={formatScore(metrics.grammar_score)}
          pillLabel={metrics.grammar_score ? getScoreLabel(metrics.grammar_score) : null}
          pillVariant={getScoreBadgeVariant(metrics.grammar_score)}
        />

        {/* Resume Score */}
        <StatCard
          title="Resume Score"
          value={formatScore(metrics.resume_score)}
          pillLabel={metrics.resume_score ? getScoreLabel(metrics.resume_score) : null}
          pillVariant={getScoreBadgeVariant(metrics.resume_score)}
        />
      </div>

      {/* 3. Middle Section: Performance Overview + AI Recommendation */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        
        {/* Performance Overview (approx 65% width / 8 cols) */}
        <Card className="lg:col-span-8 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-slate-100">
              Performance Overview
            </h2>
            <div className="relative">
              <select
                aria-label="Performance time range"
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 cursor-pointer"
              >
                <option value="week">This Week</option>
                <option value="month">This Month</option>
              </select>
            </div>
          </div>

          {/* Chart Container */}
          <div className="h-64 w-full">
            {performanceData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={performanceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="scoreAreaGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.18" />
                      <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.0" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" opacity={0.6} />
                  <XAxis
                    dataKey="label"
                    tickLine={false}
                    axisLine={false}
                    tick={{ fill: '#64748B', fontSize: 11, fontWeight: 500 }}
                  />
                  <YAxis
                    domain={[0, 100]}
                    ticks={[0, 25, 50, 75, 100]}
                    tickLine={false}
                    axisLine={false}
                    tick={{ fill: '#64748B', fontSize: 11 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1E293B',
                      border: 'none',
                      borderRadius: '12px',
                      color: '#FFF',
                      fontSize: '12px',
                      boxShadow: '0 10px 25px -5px rgba(0,0,0,0.3)',
                    }}
                    formatter={(val) => [`${val}%`, 'Score']}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#4F46E5"
                    strokeWidth={2.8}
                    dot={{ r: 4, fill: '#4F46E5', stroke: '#FFF', strokeWidth: 2 }}
                    activeDot={{ r: 6, fill: '#4338CA' }}
                    connectNulls
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                No performance data for this period yet.
              </div>
            )}
          </div>
        </Card>

        {/* AI Recommendation (approx 35% width / 4 cols) */}
        <Card className="lg:col-span-4 bg-gradient-to-br from-indigo-50/50 via-white to-white dark:from-indigo-950/20 dark:via-slate-900 dark:to-slate-900 border-indigo-100 dark:border-indigo-900/40 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-xl bg-indigo-100 dark:bg-indigo-950 border border-indigo-200/80 dark:border-indigo-800 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
                <Sparkles className="w-4 h-4 stroke-[2.2]" />
              </div>
              <h2 className="text-base font-bold text-slate-900 dark:text-slate-100">
                AI Recommendation
              </h2>
            </div>

            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed mt-2">
              {recommendation.text}
            </p>
          </div>

          <div className="pt-6">
            <Link to="/interview/setup" state={{ prefilledCategory: 'Behavioral', prefilledDifficulty: 'Intermediate' }}>
              <Button variant="primary" size="md" className="w-full font-semibold shadow-xs">
                {recommendation.action_text || 'Start Recommended Practice'}
              </Button>
            </Link>
          </div>
        </Card>

      </div>

      {/* 4. Bottom Section: Recent Interviews Table + Practice Streak / Next Goal */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        
        {/* Recent Interviews Table (approx 65% width / 8 cols) */}
        <Card className="lg:col-span-8 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-slate-100">
              Recent Interviews
            </h2>
            <Link
              to="/history"
              className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              View all
            </Link>
          </div>

          {recentSessions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs sm:text-sm">
                <thead>
                  <tr className="border-b border-slate-100 dark:border-slate-800 text-slate-400 dark:text-slate-500 font-semibold text-[11px] uppercase tracking-wider">
                    <th className="pb-3 font-semibold">Interview</th>
                    <th className="pb-3 font-semibold">Type</th>
                    <th className="pb-3 font-semibold">Score</th>
                    <th className="pb-3 font-semibold">Date</th>
                    <th className="pb-3 font-semibold text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">
                  {recentSessions.slice(0, 5).map((session) => (
                    <tr key={session.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors">
                      <td className="py-3 font-semibold text-slate-900 dark:text-slate-100">
                        {session.role_name || session.job_role_name || 'Software Engineer'}
                      </td>
                      <td className="py-3 text-slate-600 dark:text-slate-400">
                        {session.category_name || session.category || 'Technical'}
                      </td>
                      <td className="py-3">
                        {session.score !== undefined && session.score !== null ? (
                          <Badge variant={getScoreBadgeVariant(session.score)} size="sm">
                            {Math.round(session.score)}%
                          </Badge>
                        ) : session.overall_score !== undefined && session.overall_score !== null ? (
                          <Badge variant={getScoreBadgeVariant(session.overall_score)} size="sm">
                            {Math.round(session.overall_score)}%
                          </Badge>
                        ) : (
                          <span className="text-slate-400 text-xs">—</span>
                        )}
                      </td>
                      <td className="py-3 text-slate-500 text-xs">
                        {session.date || (session.created_at ? new Date(session.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recent')}
                      </td>
                      <td className="py-3 text-right">
                        <Link
                          to={`/reports/${session.id}`}
                          className="font-semibold text-xs text-indigo-600 dark:text-indigo-400 hover:underline"
                        >
                          View Report
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="py-10 text-center space-y-3">
              <p className="text-xs text-slate-400">No recent interview sessions found.</p>
              <Link to="/interview/setup">
                <Button variant="secondary" size="sm">
                  Start Your First Session
                </Button>
              </Link>
            </div>
          )}
        </Card>

        {/* Right Column: Practice Streak & Next Goal (approx 35% width / 4 cols) */}
        <div className="lg:col-span-4 space-y-4 flex flex-col justify-between">
          {/* Practice Streak Card */}
          <Card className="flex items-center justify-between p-5">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Practice Streak
              </span>
              <div className="text-2xl font-black text-slate-900 dark:text-white">
                {metrics.practice_streak_days ? `${metrics.practice_streak_days} Days` : '0 Days'}
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {metrics.practice_streak_days > 0 ? 'Keep it up!' : 'Start your streak today!'}
              </p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800 text-amber-500 flex items-center justify-center text-2xl shadow-xs">
              🔥
            </div>
          </Card>

          {/* Next Goal Card */}
          <Card className="p-5 flex-1 flex flex-col justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Next Goal
              </span>
              <p className="text-xs font-bold text-slate-800 dark:text-slate-200 mt-1">
                {metrics.next_goal?.text || 'Complete 3 interviews this week'}
              </p>
            </div>

            <div className="mt-4 space-y-2">
              <ProgressBar
                value={metrics.next_goal?.current || 1}
                max={metrics.next_goal?.target || 3}
                variant="primary"
                size="md"
              />
              <div className="flex justify-end text-[11px] font-semibold text-slate-500">
                {metrics.next_goal?.current || 1} / {metrics.next_goal?.target || 3}
              </div>
            </div>
          </Card>
        </div>

      </div>
    </div>
  );
}
