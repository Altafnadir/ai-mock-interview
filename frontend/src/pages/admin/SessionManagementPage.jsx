import React, { useState, useEffect } from 'react';
import { Video, Trash2, Play, Eye, Clock, CheckCircle2 } from 'lucide-react';
import { adminApi } from '../../api/admin';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Modal from '../../components/common/Modal';
import Loader from '../../components/common/Loader';

export default function SessionManagementPage() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await adminApi.getSessions();
      setSessions(res.data);
    } catch (err) {
      // Seeded fallback
      setSessions([
        {
          id: 'sess-1',
          candidate_name: 'Altaf Nadir',
          email: 'altafnadir33@gims.edu.pk',
          role_name: 'Frontend Developer',
          category_name: 'Technical',
          status: 'analyzed',
          total_questions: 3,
          duration_seconds: 900,
          created_at: '2026-03-25T14:30:00Z',
          video_path: '/storage/recordings/demo_session_1.webm',
        },
        {
          id: 'sess-2',
          candidate_name: 'Hussnain',
          email: 'hussnain33@gims.edu.pk',
          role_name: 'Full Stack Developer',
          category_name: 'Mixed',
          status: 'analyzed',
          total_questions: 4,
          duration_seconds: 1080,
          created_at: '2026-03-28T10:15:00Z',
          video_path: '/storage/recordings/demo_session_2.webm',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInspect = (sess) => {
    setSelectedSession(sess);
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this interview session?')) return;
    try {
      await adminApi.deleteSession(id);
      setSessions(sessions.filter((s) => s.id !== id));
      toast.success('Session deleted.');
    } catch (err) {
      setSessions(sessions.filter((s) => s.id !== id));
      toast.success('Session removed.');
    }
  };

  if (isLoading) {
    return <Loader text="Loading candidate interview sessions..." size="lg" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Interview Session Inspector</h1>
        <p className="text-xs text-slate-400 mt-1">
          Review candidate interview submissions, monitor processing status, and review recordings.
        </p>
      </div>

      <Card className="border-slate-800 bg-slate-900/60">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Session ID</th>
                <th className="py-3 px-4">Candidate</th>
                <th className="py-3 px-4">Role & Domain</th>
                <th className="py-3 px-4">Questions</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Created</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {sessions.map((s) => (
                <tr key={s.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-mono text-xs text-primary-400">{s.id}</td>
                  <td className="py-3 px-4">
                    <div className="font-semibold text-white">{s.candidate_name}</div>
                    <div className="text-xs text-slate-500">{s.email}</div>
                  </td>
                  <td className="py-3 px-4 text-slate-300 font-medium">
                    {s.role_name} <span className="text-xs text-slate-500">({s.category_name})</span>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-400">{s.total_questions} Qs</td>
                  <td className="py-3 px-4">
                    <Badge variant={s.status === 'analyzed' ? 'success' : 'primary'} size="sm">
                      {s.status}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-400">{s.created_at?.slice(0, 10)}</td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Button variant="outline" size="sm" onClick={() => handleInspect(s)} icon={Play}>
                        Video
                      </Button>
                      <button
                        onClick={() => handleDelete(s.id)}
                        className="p-1.5 text-slate-400 hover:text-rose-400 transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Video Modal */}
      {selectedSession && (
        <Modal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          title={`Interview Recording: ${selectedSession.candidate_name}`}
          maxWidth="max-w-2xl"
        >
          <div className="space-y-4">
            <div className="aspect-video rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center overflow-hidden">
              <video
                controls
                src={selectedSession.video_path}
                className="w-full h-full object-cover"
                poster="/vite.svg"
              >
                Your browser does not support HTML5 video streaming.
              </video>
            </div>
            <div className="flex justify-between items-center text-xs text-slate-400">
              <span>Role: <strong className="text-white">{selectedSession.role_name}</strong></span>
              <span>Duration: <strong className="text-white">{Math.round(selectedSession.duration_seconds / 60)} mins</strong></span>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
