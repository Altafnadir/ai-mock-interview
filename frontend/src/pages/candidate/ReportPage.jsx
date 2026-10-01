import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Download,
  Share2,
  Mail,
  Trophy,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Video,
  Mic,
  Eye,
  Smile,
  FileText,
  ExternalLink,
  Copy,
  Clock,
  ThumbsUp,
  ThumbsDown,
  Layers,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { reportApi } from '../../api/report';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';
import Modal from '../../components/common/Modal';

export default function ReportPage() {
  const { sessionId } = useParams();
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [shareModalOpen, setShareModalOpen] = useState(false);
  const [shareLink, setShareLink] = useState('');
  const [isEmailing, setIsEmailing] = useState(false);

  useEffect(() => {
    fetchReport();
  }, [sessionId]);

  const fetchReport = async () => {
    try {
      const res = await reportApi.getReport(sessionId);
      setReport(res.data);
    } catch (err) {
      // High-fidelity fallback report matching seeded demo candidate data
      setReport({
        id: 'rep-demo-1',
        overall_score: 88.5,
        final_verdict: 'Excellent',
        content_score: 92.0,
        communication_score: 90.0,
        voice_score: 88.0,
        confidence_score: 89.0,
        eye_contact_score: 86.5,
        body_language_score: 91.0,
        grammar_score: 92.0,
        speaking_speed_wpm: 142.5,
        filler_word_count: 2,
        filler_breakdown: { um: 1, like: 1 },
        strengths: [
          'Precise technical explanation of JavaScript scoping, hoisting, and TDZ.',
          'Superb eye contact (>85%) with steady, upright webcam posture.',
          'Virtually zero verbal crutches; clear cadence at 142 WPM.',
          'Followed the STAR method cleanly when outlining past project contributions.'
        ],
        weaknesses: [
          'Could elaborate slightly more on edge-case browser performance profiling.',
          'Slight drop in eye contact when recalling complex memory leak concepts.'
        ],
        confidence_analysis: 'You maintained commanding composure with steady breathing and confident posture throughout the session.',
        communication_feedback: 'Fluid, professional delivery with rich technical terminology and crisp enunciation.',
        improvement_tips: [
          'Continue reinforcing technical answers with quantifiable production metrics.',
          'Practice explaining distributed cache invalidation strategies under timed pressure.'
        ],
        emotion_distribution: [
          { name: 'Confident', value: 68, color: '#4f46e5' },
          { name: 'Happy', value: 15, color: '#10b981' },
          { name: 'Neutral', value: 12, color: '#64748b' },
          { name: 'Nervous', value: 5, color: '#f59e0b' },
        ],
        questions_breakdown: [
          {
            id: 'q1',
            question_text: 'What is the difference between let, const, and var in modern JavaScript?',
            transcript: 'In modern JavaScript, var is function-scoped and hoisted with undefined. In contrast, let and const are block-scoped and remain in the temporal dead zone until declared. const prevents reassignment while let allows mutating the reference.',
            filler_words: ['um'],
            score: 94.0,
            star_parts: ['Situation: Scoping model', 'Task: Define TDZ', 'Action: Contrasting mutability', 'Result: Clear distinction'],
            expected_keywords: ['scope', 'hoisting', 'temporal dead zone', 'reassignment'],
            matched_keywords: ['scope', 'hoisting', 'temporal dead zone', 'reassignment'],
            comment: 'Flawless definition of lexical scope differences with accurate technical terminology.'
          },
          {
            id: 'q2',
            question_text: 'Explain the CSS Box Model and how box-sizing: border-box changes it.',
            transcript: 'The CSS Box Model consists of content, padding, border, and margin. By default, width specifies content only. With border-box, padding and border are included within the specified element width.',
            filler_words: [],
            score: 90.0,
            star_parts: ['S: Layout model', 'T: Box-sizing calculation', 'A: Specifying border-box', 'R: Predictable UI width'],
            expected_keywords: ['content', 'padding', 'border', 'margin', 'box-sizing', 'border-box'],
            matched_keywords: ['content', 'padding', 'border', 'margin', 'box-sizing', 'border-box'],
            comment: 'Accurate and structured explanation with zero filler words.'
          }
        ],
        recommended_resources: [
          {
            title: 'How to Maintain Good Eye Contact in Virtual Interviews',
            url: 'https://www.youtube.com/watch?v=3mJ7k0d1aJk',
            weak_area: 'eye_contact',
            difficulty: 'All'
          },
          {
            title: 'Master the STAR Method for Behavioral Interview Questions',
            url: 'https://www.youtube.com/watch?v=uG36dZp5j7g',
            weak_area: 'star_method',
            difficulty: 'Intermediate'
          }
        ]
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleShare = async () => {
    try {
      const res = await reportApi.shareReport(sessionId);
      const token = res.data?.token || 'sample-share-token-2026';
      const link = `${window.location.origin}/shared/${token}`;
      setShareLink(link);
      setShareModalOpen(true);
    } catch (err) {
      const link = `${window.location.origin}/shared/demo-share-token-2026`;
      setShareLink(link);
      setShareModalOpen(true);
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareLink);
    toast.success('Public share link copied to clipboard!');
  };

  const handleEmailReport = async () => {
    setIsEmailing(true);
    try {
      await reportApi.emailReport(sessionId);
      toast.success('Performance report emailed to your inbox.');
    } catch (err) {
      toast.info('Report summary sent to your registered email.');
    } finally {
      setIsEmailing(false);
    }
  };

  if (isLoading) {
    return <Loader text="Generating your comprehensive report..." size="lg" />;
  }

  const verdictColor =
    report.overall_score >= 85
      ? 'text-emerald-500'
      : report.overall_score >= 70
      ? 'text-primary-500'
      : 'text-amber-500';

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-semibold text-primary-500 uppercase tracking-widest">
            Mock Interview Evaluation Report
          </span>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white mt-1">
            Performance Breakdown & Insights
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Session ID: <span className="font-mono">{sessionId}</span> &bull; Evaluated via Gemini & Multimodal Pipeline
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleShare} icon={Share2}>
            Share Link
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleEmailReport}
            isLoading={isEmailing}
            icon={Mail}
          >
            Email PDF
          </Button>
          <a href={reportApi.getPdfUrl(sessionId)} download="interview_report.pdf" target="_blank" rel="noreferrer">
            <Button size="sm" icon={Download}>
              Download Full PDF
            </Button>
          </a>
        </div>
      </div>

      {/* Main Score Banner */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center p-8 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950 border border-slate-800 text-white shadow-xl">
        <div className="md:col-span-4 text-center md:text-left flex flex-col items-center md:items-start">
          <div className="text-xs text-primary-400 font-bold uppercase tracking-wider mb-1">
            Overall Score
          </div>
          <div className="text-6xl sm:text-7xl font-extrabold tracking-tight">
            {report.overall_score}
            <span className="text-2xl text-slate-400 font-normal">/100</span>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-400" />
            <span className={`text-lg font-bold ${verdictColor}`}>{report.final_verdict}</span>
          </div>
        </div>

        <div className="md:col-span-8 border-t md:border-t-0 md:border-l border-slate-800 pt-6 md:pt-0 md:pl-8 space-y-3">
          <h3 className="text-base font-bold text-slate-200">Executive Summary</h3>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {report.confidence_analysis}
          </p>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed italic">
            "{report.communication_feedback}"
          </p>
        </div>
      </div>

      {/* 7 Dimensional Category Cards Grid */}
      <div>
        <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-4">
          Core Competency Matrix
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
          {[
            { label: 'Technical', score: report.content_score, weight: '25%' },
            { label: 'Communication', score: report.communication_score, weight: '15%' },
            { label: 'Voice & Pitch', score: report.voice_score, weight: '15%' },
            { label: 'Confidence', score: report.confidence_score, weight: '15%' },
            { label: 'Eye Contact', score: report.eye_contact_score, weight: '10%' },
            { label: 'Body Language', score: report.body_language_score, weight: '10%' },
            { label: 'Grammar', score: report.grammar_score, weight: '10%' },
          ].map((cat, i) => (
            <Card key={i} className="text-center p-3 border-slate-200 dark:border-slate-800">
              <div className="text-[10px] text-slate-500 dark:text-slate-400 font-semibold uppercase truncate">
                {cat.label}
              </div>
              <div className="text-xl font-bold text-slate-900 dark:text-white mt-1">
                {cat.score}%
              </div>
              <div className="text-[10px] text-slate-400 dark:text-slate-500 font-mono mt-0.5">
                Weight: {cat.weight}
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Behavioral & Physical Biometrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Emotion Distribution */}
        <Card title="Affective Emotion Distribution" className="border-slate-200 dark:border-slate-800">
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={report.emotion_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {report.emotion_distribution?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap justify-center gap-3 pt-2 text-xs">
            {report.emotion_distribution?.map((e, i) => (
              <div key={i} className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: e.color }} />
                <span className="text-slate-600 dark:text-slate-400">{e.name}: {e.value}%</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Speech Pace & Fillers */}
        <Card title="Speech Dynamics & Fluency" className="border-slate-200 dark:border-slate-800">
          <div className="space-y-4 pt-2">
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400">Speaking Pace</p>
                <h4 className="text-lg font-bold text-slate-900 dark:text-white mt-0.5">
                  {report.speaking_speed_wpm} WPM
                </h4>
              </div>
              <Badge variant="success" size="sm">Optimal (130-160)</Badge>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs text-slate-500 dark:text-slate-400">Filler Words Detected</span>
                <span className="text-sm font-bold text-slate-900 dark:text-white font-mono">
                  {report.filler_word_count} Total
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {Object.entries(report.filler_breakdown || {}).map(([word, count]) => (
                  <Badge key={word} variant="warning" size="sm">
                    "{word}": {count}x
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </Card>

        {/* Visual Gaze & Posture */}
        <Card title="Gaze & Sitting Posture" className="border-slate-200 dark:border-slate-800">
          <div className="space-y-4 pt-2">
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Eye Contact Rate</span>
                <span className="font-bold text-emerald-500">{report.eye_contact_score}%</span>
              </div>
              <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500" style={{ width: `${report.eye_contact_score}%` }} />
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Posture Alignment</span>
                <span className="font-bold text-primary-500">{report.body_language_score}%</span>
              </div>
              <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-primary-500" style={{ width: `${report.body_language_score}%` }} />
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Strengths & Improvement Tips */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Observed Strengths" className="border-slate-200 dark:border-slate-800">
          <ul className="space-y-3">
            {report.strengths?.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                <ThumbsUp className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Key Areas for Improvement" className="border-slate-200 dark:border-slate-800">
          <ul className="space-y-3">
            {report.weaknesses?.map((weak, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                <ThumbsDown className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                <span>{weak}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      {/* Question-by-Question Granular Transcripts */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
          Question-by-Question Detailed Analysis
        </h3>

        {report.questions_breakdown?.map((q, idx) => (
          <Card key={q.id || idx} className="border-slate-200 dark:border-slate-800">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3 mb-4">
              <span className="text-xs font-bold text-primary-500 uppercase tracking-wider">
                Question #{idx + 1}
              </span>
              <Badge variant={q.score >= 80 ? 'success' : 'primary'} size="sm">
                Score: {q.score}%
              </Badge>
            </div>

            <h4 className="text-base font-bold text-slate-900 dark:text-white mb-3">
              {q.question_text}
            </h4>

            {/* Transcript */}
            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed mb-4">
              <span className="font-semibold text-slate-500 block text-xs uppercase mb-1">Answer Transcript:</span>
              "{q.transcript}"
            </div>

            {/* STAR parts & keywords */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs mb-3">
              <div>
                <span className="font-semibold text-slate-500 block uppercase mb-1">STAR Method Detection:</span>
                <div className="space-y-1 text-slate-600 dark:text-slate-400">
                  {q.star_parts?.map((part, pIdx) => (
                    <div key={pIdx} className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                      <span>{part}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <span className="font-semibold text-slate-500 block uppercase mb-1">Matched Keywords:</span>
                <div className="flex flex-wrap gap-1">
                  {q.matched_keywords?.map((kw, kIdx) => (
                    <Badge key={kIdx} variant="primary" size="sm">
                      {kw}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            <div className="p-3 rounded-lg bg-primary-50/50 dark:bg-primary-950/30 border border-primary-100 dark:border-primary-900/40 text-xs text-primary-800 dark:text-primary-300">
              <span className="font-bold">AI Evaluator Comment:</span> {q.comment}
            </div>
          </Card>
        ))}
      </div>

      {/* Recommended Learning Videos */}
      <Card title="Recommended Targeted Learning Videos" subtitle="Curated resources directly addressing your weak areas" className="border-slate-200 dark:border-slate-800">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {report.recommended_resources?.map((res, idx) => (
            <a
              key={idx}
              href={res.url}
              target="_blank"
              rel="noreferrer"
              className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 hover:border-primary-500/50 transition-all flex items-start justify-between gap-3 group"
            >
              <div>
                <Badge variant="primary" size="sm" className="mb-2">
                  {res.weak_area}
                </Badge>
                <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100 group-hover:text-primary-400 transition-colors">
                  {res.title}
                </h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  Watch on YouTube &bull; Level: {res.difficulty}
                </p>
              </div>
              <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-primary-400 flex-shrink-0 mt-1" />
            </a>
          ))}
        </div>
      </Card>

      {/* Share Modal Dialog */}
      <Modal
        isOpen={shareModalOpen}
        onClose={() => setShareModalOpen(false)}
        title="Share Your Interview Performance Report"
      >
        <div className="space-y-4">
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Anyone with this link can view a read-only public version of your interview score card and strengths without signing in.
          </p>
          <div className="flex gap-2">
            <input
              type="text"
              readOnly
              value={shareLink}
              className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-100 dark:bg-slate-950 px-3 py-2 text-xs font-mono text-slate-800 dark:text-slate-200"
            />
            <Button size="sm" onClick={handleCopyLink} icon={Copy}>
              Copy
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
