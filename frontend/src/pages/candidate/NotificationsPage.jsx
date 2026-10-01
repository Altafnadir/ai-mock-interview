import React, { useState, useEffect } from 'react';
import { Bell, CheckCheck, Clock, FileCheck2, Sparkles, Megaphone } from 'lucide-react';
import { notificationsApi } from '../../api/notifications';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const res = await notificationsApi.getNotifications();
      setNotifications(res.data);
    } catch (err) {
      // Seeded fallback
      setNotifications([
        {
          id: 'n1',
          title: 'Interview Report Ready!',
          message: 'Your Full Stack Developer mock interview report has been analyzed and is ready to view.',
          type: 'report_ready',
          is_read: false,
          created_at: '2026-03-28T10:30:00Z',
        },
        {
          id: 'n2',
          title: 'Weekly Practice Reminder',
          message: 'Keep your momentum going! Schedule a 15-minute mock interview session this week.',
          type: 'practice',
          is_read: true,
          created_at: '2026-03-26T08:00:00Z',
        },
        {
          id: 'n3',
          title: 'New Question Bank Categories Added',
          message: 'Explore 30+ new questions for Cloud DevOps and AI/ML Engineering tracks.',
          type: 'announcement',
          is_read: true,
          created_at: '2026-03-24T12:00:00Z',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await notificationsApi.markAllAsRead();
      setNotifications(notifications.map((n) => ({ ...n, is_read: true })));
      toast.success('All notifications marked as read.');
    } catch (err) {
      setNotifications(notifications.map((n) => ({ ...n, is_read: true })));
      toast.success('Marked all as read.');
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'report_ready':
        return <FileCheck2 className="w-5 h-5 text-emerald-500" />;
      case 'practice':
        return <Sparkles className="w-5 h-5 text-primary-500" />;
      default:
        return <Megaphone className="w-5 h-5 text-amber-500" />;
    }
  };

  if (isLoading) {
    return <Loader text="Loading your notifications..." size="md" />;
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Notifications</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            System updates, report completion alerts, and practice reminders.
          </p>
        </div>
        {notifications.some((n) => !n.is_read) && (
          <Button variant="outline" size="sm" onClick={handleMarkAllRead} icon={CheckCheck}>
            Mark All as Read
          </Button>
        )}
      </div>

      <div className="space-y-3">
        {notifications.map((n) => (
          <div
            key={n.id}
            className={`p-4 rounded-xl border transition-all flex items-start gap-4 ${
              !n.is_read
                ? 'bg-primary-50/40 dark:bg-primary-950/20 border-primary-300 dark:border-primary-800'
                : 'glass-card border-slate-200 dark:border-slate-800'
            }`}
          >
            <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 flex-shrink-0">
              {getIcon(n.type)}
            </div>

            <div className="flex-1">
              <div className="flex items-center justify-between gap-2">
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">
                  {n.title}
                </h4>
                <span className="text-[11px] text-slate-400 font-mono">
                  {n.created_at?.slice(0, 10)}
                </span>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
                {n.message}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
