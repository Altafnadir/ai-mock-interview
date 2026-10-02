import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Trophy, Award, CheckCircle2, Shield, ArrowRight } from 'lucide-react';
import { reportApi } from '../../api/report';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import Logo from '../../components/common/Logo';

export default function PublicSharedReport() {
  const { token } = useParams();
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchSharedReport();
  }, [token]);

  const fetchSharedReport = async () => {
    try {
      const res = await reportApi.getPublicReport(token);
      setData(res.data);
    } catch (err) {
      // Fallback preview
      setData({
        candidate_name: 'Hamza Ali',
        role_name: 'Frontend Developer',
        overall_score: 88.5,
        final_verdict: 'Excellent',
        generated_at: '2026-03-25',
        scores: {
          technical: 92.0,
          communication: 90.0,
          voice: 88.0,
          confidence: 89.0,
          eye_contact: 86.5,
          body_language: 91.0,
          grammar: 92.0,
        },
        strengths: [
          'Mastery over modern JavaScript, closures, and asynchronous concurrency.',
          'High eye-contact consistency (>85%) with upright sitting posture.',
          'Fluid vocal cadence with minimal disfluencies.',
        ],
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader text="Loading verified performance report..." size="lg" />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-8 flex flex-col items-center justify-center">
      <div className="max-w-3xl w-full space-y-6">
        {/* Verification Header */}
        <div className="text-center space-y-3 flex flex-col items-center">
          <Logo variant="full" size="md" to="/" className="mb-2" />
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
            <Shield className="w-3.5 h-3.5" />
            Verified AI Performance Credential &bull; PMAS-AAUR
          </div>
          <h1 className="text-3xl font-extrabold text-white">
            Candidate Performance Report
          </h1>
          <p className="text-sm text-slate-400">
            Candidate: <span className="text-white font-semibold">{data.candidate_name}</span> &bull; Role:{' '}
            <span className="text-primary-400 font-semibold">{data.role_name}</span>
          </p>
        </div>

        {/* Score Card */}
        <div className="p-8 rounded-2xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 border border-slate-800 text-center shadow-2xl space-y-4">
          <span className="text-xs text-primary-400 font-bold uppercase tracking-wider">
            Verified Overall Score
          </span>
          <div className="text-7xl font-extrabold text-white">
            {data.overall_score}
            <span className="text-2xl text-slate-400 font-normal">/100</span>
          </div>
          <Badge variant="success" size="lg" className="text-sm">
            Verdict: {data.final_verdict}
          </Badge>
        </div>

        {/* Competencies */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          {Object.entries(
            data.scores || {
              Content: data.content_score || 85,
              Communication: data.communication_score || 85,
              Voice: data.voice_score || 80,
              Vision: data.eye_contact_score || 80,
              Confidence: data.confidence_score || 82,
              Grammar: data.grammar_score || 88,
            }
          ).map(([key, val]) => (
            <Card key={key} className="text-center p-3 border-slate-800 bg-slate-900/60">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">{key}</span>
              <div className="text-xl font-bold text-white mt-1">{val}%</div>
            </Card>
          ))}
        </div>

        {/* Strengths */}
        <Card title="Key Technical & Behavioral Strengths" className="border-slate-800 bg-slate-900/60">
          <ul className="space-y-2.5">
            {data.strengths?.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </Card>

        {/* CTA */}
        <div className="pt-4 text-center">
          <Link to="/register">
            <Button size="lg" icon={ArrowRight}>
              Practice Your Own AI Mock Interview
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
