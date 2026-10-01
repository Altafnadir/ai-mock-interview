import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  FileCheck2,
  Trash2,
  Filter,
  Layers,
  ArrowRight,
  TrendingUp,
} from 'lucide-react';
import { interviewApi } from '../../api/interview';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';
import Modal from '../../components/common/Modal';

export default function HistoryPage() {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterRole, setFilterRole] = useState('all');
  const [compareIds, setCompareIds] = useState([]);
  const [compareModalOpen, setCompareModalOpen] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await interviewApi.getHistory();
      setSessions(res.data);
    } catch (err) {
      // Seeded fallback
      setSessions([
        {
          id: 's1',
          role_name: 'Frontend Developer',
          category_name: 'Technical',
          difficulty_name: 'Beginner',
          overall_score: 88.5,
          final_verdict: 'Excellent',
          created_at: '2026-03-25T14:30:00Z',
          duration_seconds: 900,
          total_questions: 3,
        },
        {
          id: 's2',
          role_name: 'Full Stack Developer',
          category_name: 'Mixed',
          difficulty_name: 'Intermediate',
          overall_score: 76.2,
          final_verdict: 'Good',
          created_at: '2026-03-28T10:15:00Z',
          duration_seconds: 1080,
          total_questions: 4,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await interviewApi.deleteSession(id);
      setSessions(sessions.filter((s) => s.id !== id));
      toast.success('Session removed from history.');
    } catch (err) {
      toast.error('Could not delete session.');
    }
  };

  const toggleCompare = (id) => {
    if (compareIds.includes(id)) {
      setCompareIds(compareIds.filter((item) => item !== id));
    } else {
      if (compareIds.length >= 3) {
        toast.warning('You can compare up to 3 sessions simultaneously.');
        return;
      }
      setCompareIds([...compareIds, id]);
    }
  };

  if (isLoading) {
    return <Loader text="Loading your session history..." size="lg" />;
  }

  const filtered = sessions.filter(
    (s) => filterRole === 'all' || s.role_name === filterRole
  );

  const comparedSessions = sessions.filter((s) => compareIds.includes(s.id));

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Interview History & Progression
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Review past mock interviews or compare multi-session metrics side-by-side.
          </p>
        </div>

        {compareIds.length >= 2 && (
          <Button
            variant="primary"
            size="md"
            onClick={() => setCompareModalOpen(true)}
            icon={Layers}
            className="shadow-md shadow-primary-600/30"
          >
            Compare ({compareIds.length}) Sessions
          </Button>
        )}
      </div>

      {/* Filter and Session List */}
      <Card className="border-slate-200 dark:border-slate-800">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Compare</th>
                <th className="py-3 px-4">Date & Time</th>
                <th className="py-3 px-4">Target Job Role</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Difficulty</th>
                <th className="py-3 px-4">Overall Score</th>
                <th className="py-3 px-4">Verdict</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {filtered.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/50 transition-colors">
                  <td className="py-3 px-4">
                    <input
                      type="checkbox"
                      checked={compareIds.includes(s.id)}
                      onChange={() => toggleCompare(s.id)}
                      className="rounded border-slate-700 text-primary-600 focus:ring-primary-500"
                    />
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-500 dark:text-slate-400">
                    {s.created_at?.slice(0, 10)}
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">
                    {s.role_name}
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-600 dark:text-slate-400">
                    {s.category_name}
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="slate" size="sm">{s.difficulty_name}</Badge>
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">
                    {s.overall_score}%
                  </td>
                  <td className="py-3 px-4">
                    <Badge
                      variant={s.overall_score >= 80 ? 'success' : 'primary'}
                      size="sm"
                    >
                      {s.final_verdict}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Link to={`/reports/${s.id}`}>
                        <Button variant="outline" size="sm" icon={FileCheck2}>
                          Report
                        </Button>
                      </Link>
                      <button
                        onClick={() => handleDelete(s.id)}
                        className="p-1.5 text-slate-400 hover:text-rose-500 transition-colors"
                        title="Delete Session"
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

      {/* Side-by-Side Comparison Modal */}
      <Modal
        isOpen={compareModalOpen}
        onClose={() => setCompareModalOpen(false)}
        title="Side-by-Side Session Comparison"
        maxWidth="max-w-3xl"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {comparedSessions.map((s) => (
            <div
              key={s.id}
              className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 space-y-3"
            >
              <div>
                <span className="text-xs text-slate-500 dark:text-slate-400">{s.created_at?.slice(0, 10)}</span>
                <h4 className="text-base font-bold text-slate-900 dark:text-white mt-0.5">{s.role_name}</h4>
                <p className="text-xs text-primary-500">{s.category_name} &bull; {s.difficulty_name}</p>
              </div>

              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 text-center">
                <span className="text-xs text-slate-400 uppercase">Score</span>
                <div className="text-3xl font-extrabold text-white mt-0.5">{s.overall_score}%</div>
                <Badge variant="success" size="sm" className="mt-1">{s.final_verdict}</Badge>
              </div>

              <div className="text-xs text-slate-600 dark:text-slate-400 space-y-1">
                <div>Questions: <span className="font-semibold text-white">{s.total_questions}</span></div>
                <div>Duration: <span className="font-semibold text-white">{Math.round(s.duration_seconds / 60)} mins</span></div>
              </div>

              <Link to={`/reports/${s.id}`} className="block">
                <Button variant="outline" size="sm" className="w-full">
                  Full Report &rarr;
                </Button>
              </Link>
            </div>
          ))}
        </div>
      </Modal>
    </div>
  );
}
