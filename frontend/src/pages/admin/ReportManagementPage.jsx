import React, { useState, useEffect } from 'react';
import { FileCheck2, Download, ExternalLink, Trophy } from 'lucide-react';
import { adminApi } from '../../api/admin';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';

export default function ReportManagementPage() {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await adminApi.getReports();
      setReports(res.data);
    } catch (err) {
      // Seeded fallback
      setReports([
        {
          id: 'rep-1',
          session_id: 's1',
          candidate_name: 'Hamza Ali (Demo Candidate)',
          role_name: 'Frontend Developer',
          overall_score: 88.5,
          final_verdict: 'Excellent',
          generated_at: '2026-03-25T14:45:00Z',
          scores: { technical: 92, communication: 90, voice: 88, eye: 86.5 },
        },
        {
          id: 'rep-2',
          session_id: 's2',
          candidate_name: 'Hamza Ali (Demo Candidate)',
          role_name: 'Full Stack Developer',
          overall_score: 76.2,
          final_verdict: 'Good',
          generated_at: '2026-03-28T10:35:00Z',
          scores: { technical: 79, communication: 75, voice: 75, eye: 72 },
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader text="Loading reports archive..." size="lg" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Generated Reports Archive</h1>
        <p className="text-xs text-slate-400 mt-1">
          Inspect student performance reports, scores, and download official PDF documents.
        </p>
      </div>

      <Card className="border-slate-800 bg-slate-900/60">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Candidate</th>
                <th className="py-3 px-4">Job Role</th>
                <th className="py-3 px-4">Score</th>
                <th className="py-3 px-4">Verdict</th>
                <th className="py-3 px-4">Generated At</th>
                <th className="py-3 px-4 text-right">PDF Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {reports.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-semibold text-white">{r.candidate_name}</td>
                  <td className="py-3 px-4 text-slate-300 font-medium">{r.role_name}</td>
                  <td className="py-3 px-4 font-bold text-white">{r.overall_score}%</td>
                  <td className="py-3 px-4">
                    <Badge variant={r.overall_score >= 80 ? 'success' : 'primary'} size="sm">
                      {r.final_verdict}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-400">{r.generated_at?.slice(0, 10)}</td>
                  <td className="py-3 px-4 text-right">
                    <a
                      href={`/api/v1/reports/${r.session_id}/pdf`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      <Button variant="outline" size="sm" icon={Download}>
                        Download PDF
                      </Button>
                    </a>
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
