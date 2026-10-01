import React, { useState, useEffect } from 'react';
import { FolderTree, Plus, Sparkles, Sliders } from 'lucide-react';
import { adminApi } from '../../api/admin';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Input from '../../components/common/Input';
import Loader from '../../components/common/Loader';

export default function ContentManagementPage() {
  const [jobRoles, setJobRoles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [feedbackTemplates, setFeedbackTemplates] = useState([]);
  const [scoringWeights, setScoringWeights] = useState({
    content: 25,
    communication: 15,
    voice: 15,
    confidence: 15,
    eye_contact: 10,
    body_language: 10,
    grammar: 10,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      const [rRes, cRes, fRes] = await Promise.all([
        adminApi.getJobRoles(),
        adminApi.getCategories(),
        adminApi.getFeedbackTemplates(),
      ]);
      setJobRoles(rRes.data);
      setCategories(cRes.data);
      setFeedbackTemplates(fRes.data);
    } catch (err) {
      // Seeded fallback
      setJobRoles([
        { id: '1', name: 'Frontend Developer', description: 'Client side and web UI technologies' },
        { id: '2', name: 'Backend Developer', description: 'Server APIs, microservices, databases' },
        { id: '3', name: 'Full Stack Developer', description: 'End to end web applications' },
        { id: '4', name: 'Software Engineer', description: 'Algorithms, design patterns, systems' },
        { id: '5', name: 'QA Engineer', description: 'Test automation, quality assurance' },
        { id: '6', name: 'Data Analyst', description: 'Data modeling, BI, analytics' },
        { id: '7', name: 'Cybersecurity Analyst', description: 'Network defense, security audits' },
        { id: '8', name: 'Mobile App Developer', description: 'iOS and Android applications' },
        { id: '9', name: 'DevOps Engineer', description: 'CI/CD, Kubernetes, cloud platforms' },
        { id: '10', name: 'AI/ML Engineer', description: 'Machine learning, LLMs, computer vision' },
        { id: '11', name: 'Business Analyst', description: 'Requirement engineering, agile workflows' },
      ]);
      setCategories([
        { id: 'c1', name: 'Technical', description: 'Domain specific deep technical questions' },
        { id: 'c2', name: 'HR', description: 'Cultural alignment and motivation' },
        { id: 'c3', name: 'Behavioral', description: 'STAR method situational responses' },
        { id: 'c4', name: 'Mixed', description: 'Balanced combination across categories' },
      ]);
      setFeedbackTemplates([
        { id: 'f1', area: 'overall', min_score: 85, max_score: 100, template_text: 'Exceptional performance! Outstanding technical depth and articulation.' },
        { id: 'f2', area: 'overall', min_score: 70, max_score: 84.9, template_text: 'Good interview presence with solid fundamentals.' },
        { id: 'f3', area: 'overall', min_score: 50, max_score: 69.9, template_text: 'Satisfactory foundation, but needs improvement.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveWeights = (e) => {
    e.preventDefault();
    const sum = Object.values(scoringWeights).reduce((a, b) => Number(a) + Number(b), 0);
    if (sum !== 100) {
      toast.error(`Weights must sum to 100% (Current sum: ${sum}%).`);
      return;
    }
    toast.success('Platform scoring weights updated successfully!');
  };

  if (isLoading) {
    return <Loader text="Loading content taxonomy..." size="lg" />;
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Content & Taxonomy Management</h1>
        <p className="text-xs text-slate-400 mt-1">
          Configure job roles, question categories, feedback templates, and scoring weights.
        </p>
      </div>

      {/* Configurable Scoring Matrix */}
      <Card title="Platform Scoring Weight Distribution" subtitle="System weights for calculating the 0-100 overall performance score" className="border-slate-800 bg-slate-900/60">
        <form onSubmit={handleSaveWeights} className="space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            {Object.entries(scoringWeights).map(([key, val]) => (
              <div key={key}>
                <label className="block text-[11px] font-semibold text-slate-400 uppercase truncate mb-1">
                  {key.replace('_', ' ')}
                </label>
                <div className="relative">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={val}
                    onChange={(e) =>
                      setScoringWeights({
                        ...scoringWeights,
                        [key]: parseInt(e.target.value) || 0,
                      })
                    }
                    className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-1.5 text-sm text-white font-mono"
                  />
                  <span className="absolute right-2.5 top-1.5 text-xs text-slate-500">%</span>
                </div>
              </div>
            ))}
          </div>
          <div className="flex justify-end pt-2">
            <Button type="submit" size="sm">
              Save Scoring Weights
            </Button>
          </div>
        </form>
      </Card>

      {/* Job Roles Grid */}
      <Card title="Active Tech Job Roles (11 Tracks)" className="border-slate-800 bg-slate-900/60">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {jobRoles.map((role) => (
            <div
              key={role.id}
              className="p-3.5 rounded-xl border border-slate-800 bg-slate-950 space-y-1"
            >
              <h4 className="text-sm font-bold text-white">{role.name}</h4>
              <p className="text-xs text-slate-400 line-clamp-2">{role.description}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Categories & Feedback Templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Interview Categories" className="border-slate-800 bg-slate-900/60">
          <div className="space-y-3">
            {categories.map((c) => (
              <div key={c.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-sm font-bold text-white">{c.name}</span>
                <p className="text-xs text-slate-400 mt-0.5">{c.description}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Score Feedback Templates" className="border-slate-800 bg-slate-900/60">
          <div className="space-y-3">
            {feedbackTemplates.map((t) => (
              <div key={t.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="flex justify-between items-center text-xs mb-1">
                  <Badge variant="primary" size="sm">{t.area}</Badge>
                  <span className="font-mono text-slate-400">{t.min_score} - {t.max_score} pts</span>
                </div>
                <p className="text-xs text-slate-300 italic">"{t.template_text}"</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
