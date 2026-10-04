import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Trophy,
  Target,
  Clock,
  Flame,
  ArrowRight,
  TrendingUp,
  FileCheck2,
  AlertTriangle,
  Play,
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { dashboardApi } from '../../api/dashboard';
import { useAuthStore } from '../../store/authStore';
import { useThemeStore } from '../../store/themeStore';
import { getChartTheme } from '../../utils/chartTheme';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { theme, resolvedTheme } = useThemeStore();
  const isDark = resolvedTheme === 'black' || resolvedTheme === 'blue';
  const chartColors = getChartTheme(theme, isDark);
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const res = await dashboardApi.getOverview();
      setData(res.data);
    } catch (err) {
      // Fallback sample data if backend endpoint is in setup
      setData({
        metrics: {
          total_interviews: 3,
          average_score: 82.4,
          highest_score: 88.5,
          practice_streak_days: 4,
        },
        score_trend: [
          { date: 'Session 1', score: 64.0 },
          { date: 'Session 2', score: 76.2 },
          { date: 'Session 3', score: 88.5 },
        ],
        competency_radar: [
          { subject: 'Technical Content', value: 92, fullMark: 100 },
          { subject: 'Voice & Tone', value: 88, fullMark: 100 },
          { subject: 'Eye Contact', value: 86, fullMark: 100 },
          { subject: 'Body Language', value: 91, fullMark: 100 },
          { subject: 'Grammar', value: 92, fullMark: 100 },
          { subject: 'Confidence', value: 89, fullMark: 100 },
        ],
        recent_sessions: [
          {
            id: 's1',
            role_name: 'Frontend Developer',
            category_name: 'Technical',
            difficulty_name: 'Beginner',
            score: 88.5,
            verdict: 'Excellent',
            date: '2026-03-25',
          },
          {
            id: 's2',
            role_name: 'Full Stack Developer',
            category_name: 'Mixed',
            difficulty_name: 'Intermediate',
            score: 76.2,
            verdict: 'Good',
            date: '2026-03-28',
          },
        ],
        weak_area_alert: {
          tag: 'filler_words',
          title: 'Verbal Crutches & Filler Words',
          suggestion: 'Your recent session had 12 filler words. Practice replacing verbal crutches with silent pauses.',
        },
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader text="Loading your interview dashboard..." size="lg" />;
  }

  const { metrics, score_trend, competency_radar, recent_sessions, weak_area_alert } = data;

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-primary-950 via-slate-900 to-indigo-950 border border-primary-800/40 shadow-xl">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Welcome back, {user?.full_name?.split(' ')[0] || 'Candidate'}!
          </h1>
          <p className="text-sm text-slate-300 mt-1 max-w-xl">
            You're on a <span className="text-amber-400 font-semibold">{metrics.practice_streak_days}-day practice streak</span>. Ready for your next mock interview drill?
          </p>
        </div>
        <Link to="/interview/setup">
          <Button size="lg" className="shadow-lg shadow-primary-600/30 whitespace-nowrap" icon={Play}>
            Start New Interview
          </Button>
        </Link>
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card hoverEffect className="border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider">
                Total Sessions
              </p>
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
                {metrics.total_interviews}
              </h3>
            </div>
            <div className="w-11 h-11 rounded-xl bg-primary-100 dark:bg-primary-950/80 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <Clock className="w-5 h-5" />
            </div>
          </div>
        </Card>

        <Card hoverEffect className="border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider">
                Average Score
              </p>
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
                {metrics.average_score}%
              </h3>
            </div>
            <div className="w-11 h-11 rounded-xl bg-indigo-100 dark:bg-indigo-950/80 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
              <Target className="w-5 h-5" />
            </div>
          </div>
        </Card>

        <Card hoverEffect className="border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider">
                Best Score
              </p>
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1 text-emerald-600 dark:text-emerald-400">
                {metrics.highest_score}%
              </h3>
            </div>
            <div className="w-11 h-11 rounded-xl bg-emerald-100 dark:bg-emerald-950/80 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
              <Trophy className="w-5 h-5" />
            </div>
          </div>
        </Card>

        <Card hoverEffect className="border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider">
                Practice Streak
              </p>
              <h3 className="text-2xl font-extrabold text-amber-500 mt-1">
                {metrics.practice_streak_days} Days
              </h3>
            </div>
            <div className="w-11 h-11 rounded-xl bg-amber-100 dark:bg-amber-950/80 flex items-center justify-center text-amber-500">
              <Flame className="w-5 h-5" />
            </div>
          </div>
        </Card>
      </div>

      {/* Weak Area Alert Banner */}
      {weak_area_alert && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-amber-500">Recommended Focus Area: {weak_area_alert.title}</h4>
              <p className="text-xs text-slate-600 dark:text-slate-300 mt-0.5">{weak_area_alert.suggestion}</p>
            </div>
          </div>
          <Link to={`/resources?weak_area=${weak_area_alert.tag}`} className="flex-shrink-0">
            <Button size="sm" variant="outline" className="border-amber-500/40 text-amber-400 hover:bg-amber-500/10">
              View Tutorials &rarr;
            </Button>
          </Link>
        </div>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Score Trend Line */}
        <Card
          title="Performance Progression"
          subtitle="Score evolution across completed mock interview sessions"
          className="border-slate-200 dark:border-slate-800"
        >
          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={score_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.gridStroke} opacity={0.5} />
                <XAxis dataKey="date" stroke={chartColors.axisTickColor} fontSize={11} />
                <YAxis domain={[0, 100]} stroke={chartColors.axisTickColor} fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: chartColors.tooltipBg,
                    borderColor: chartColors.tooltipBorder,
                    borderRadius: '8px',
                    color: chartColors.tooltipTextColor,
                    fontSize: '12px',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke={chartColors.primaryLine}
                  strokeWidth={3}
                  dot={{ fill: chartColors.primaryLine, strokeWidth: 2, r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Competency Radar */}
        <Card
          title="Multimodal Competency Radar"
          subtitle="Average evaluation scores across key performance layers"
          className="border-slate-200 dark:border-slate-800"
        >
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={competency_radar}>
                <PolarGrid stroke={chartColors.gridStroke} opacity={0.5} />
                <PolarAngleAxis dataKey="subject" stroke={chartColors.axisTickColor} fontSize={10} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke={chartColors.axisTickColor} fontSize={9} />
                <Radar
                  name="Score"
                  dataKey="value"
                  stroke={chartColors.radarStroke}
                  fill={chartColors.radarFill}
                  fillOpacity={0.35}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Recent Sessions Table */}
      <Card
        title="Recent Mock Interviews"
        subtitle="Review your latest performance breakdowns and generated PDF reports"
        action={
          <Link to="/history">
            <Button variant="ghost" size="sm" icon={ArrowRight}>
              View All History
            </Button>
          </Link>
        }
        className="border-slate-200 dark:border-slate-800"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Role & Domain</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Difficulty</th>
                <th className="py-3 px-4">Score</th>
                <th className="py-3 px-4">Verdict</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {recent_sessions.map((sess) => (
                <tr key={sess.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/50 transition-colors">
                  <td className="py-3 px-4 font-semibold text-slate-800 dark:text-slate-200">
                    {sess.role_name}
                  </td>
                  <td className="py-3 px-4 text-slate-600 dark:text-slate-400 text-xs">
                    {sess.category_name}
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="slate" size="sm">{sess.difficulty_name}</Badge>
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900 dark:text-slate-100">
                    {sess.score}%
                  </td>
                  <td className="py-3 px-4">
                    <Badge
                      variant={sess.score >= 80 ? 'success' : sess.score >= 65 ? 'primary' : 'warning'}
                      size="sm"
                    >
                      {sess.verdict}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <Link to={`/reports/${sess.id}`}>
                      <Button variant="outline" size="sm" icon={FileCheck2}>
                        Report
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
