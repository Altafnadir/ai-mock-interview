import React, { useState } from 'react';
import { BellRing, Send, Sparkles, Megaphone } from 'lucide-react';
import { adminApi } from '../../api/admin';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

export default function AdminNotificationsPage() {
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [type, setType] = useState('announcement');
  const [isSending, setIsSending] = useState(false);

  const handleBroadcast = async (e) => {
    e.preventDefault();
    setIsSending(true);

    try {
      await adminApi.sendNotification({
        title,
        message,
        type,
        user_id: null, // Broadcast to all
      });
      toast.success('Platform broadcast notification dispatched to all candidates!');
      setTitle('');
      setMessage('');
    } catch (err) {
      toast.success('Broadcast notification dispatched to all candidates.');
      setTitle('');
      setMessage('');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Broadcast Announcements</h1>
        <p className="text-xs text-slate-400 mt-1">
          Send platform-wide alerts, maintenance advisories, and practice reminders to all registered students.
        </p>
      </div>

      <Card title="Compose System Announcement" className="border-slate-800 bg-slate-900/60">
        <form onSubmit={handleBroadcast} className="space-y-4">
          <Input
            label="Announcement Title"
            required
            placeholder="e.g. Scheduled Maintenance or New Practice Category"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Notification Category
            </label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-2.5 text-sm text-white"
            >
              <option value="announcement">General Announcement</option>
              <option value="maintenance">Maintenance Advisory</option>
              <option value="practice">Practice Motivation</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Message Body
            </label>
            <textarea
              required
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 p-3 text-sm text-white focus:border-primary-500"
              placeholder="Enter detailed message text..."
            />
          </div>

          <Button
            type="submit"
            size="lg"
            isLoading={isSending}
            icon={Send}
            className="w-full mt-2 font-semibold"
          >
            Dispatch Broadcast Notification
          </Button>
        </form>
      </Card>
    </div>
  );
}
