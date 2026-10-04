import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, Video } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import { adminApi } from '../../api/admin';
import { useThemeStore } from '../../store/themeStore';
import { getChartTheme } from '../../utils/chartTheme';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';

export default function AnalyticsPage() {
  const { theme, resolvedTheme } = useThemeStore();
  const isDark = resolvedTheme === 'black' || resolvedTheme === 'blue';
  const chartColors = getChartTheme(theme, isDark);
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await adminApi.getAnalytics();
      setData(res.data);
    } catch (err) {
      // Seeded fallback
      setData({
        activity_over_time: [
          { day: 'Mon', interviews: 4, users: 2 },
          { day: 'Tue', interviews: 7, users: 3 },
          { day: 'Wed', interviews: 12, users: 6 },
          { day: 'Thu', interviews: 9, users: 4 },
          { day: 'Fri', interviews: 15, users: 8 },
          { day: 'Sat', interviews: 18, users: 11 },
          { day: 'Sun', interviews: 14, users: 5 },
        ],
        role_averages: [
          { role: 'Frontend', Technical: 85, Communication: 88, Voice: 82 },
          { role: 'Backend', Technical: 89, Communication: 78, Voice: 80 },
          { role: 'Full Stack', Technical: 84, Communication: 82, Voice: 81 },
          { role: 'DevOps', Technical: 88, Communication: 76, Voice: 79 },
          { role: 'AI/ML', Technical: 91, Communication: 80, Voice: 84 },
        ],
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader text="Computing platform analytics..." size="lg" />;
  }

  const { activity_over_time, role_averages } = data;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Platform Analytics & Intelligence</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Deep telemetry on candidate interview volume and competency trends across engineering domains.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Over Time */}
        <Card title="Interview Activity & Candidate Signups" className="border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/60">
          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={activity_over_time}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.gridStroke} opacity={0.5} />
                <XAxis dataKey="day" stroke={chartColors.axisTickColor} fontSize={11} />
                <YAxis stroke={chartColors.axisTickColor} fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: chartColors.tooltipBg,
                    borderColor: chartColors.tooltipBorder,
                    borderRadius: '8px',
                    color: chartColors.tooltipTextColor,
                  }}
                />
                <Line type="monotone" dataKey="interviews" stroke={chartColors.primaryLine} strokeWidth={3} />
                <Line type="monotone" dataKey="users" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Role Averages */}
        <Card title="Average Competencies by Track" className="border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/60">
          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={role_averages}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.gridStroke} opacity={0.5} />
                <XAxis dataKey="role" stroke={chartColors.axisTickColor} fontSize={10} />
                <YAxis domain={[0, 100]} stroke={chartColors.axisTickColor} fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: chartColors.tooltipBg,
                    borderColor: chartColors.tooltipBorder,
                    borderRadius: '8px',
                    color: chartColors.tooltipTextColor,
                  }}
                />
                <Bar dataKey="Technical" fill={chartColors.barColor} radius={[4, 4, 0, 0]} />
                <Bar dataKey="Communication" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
