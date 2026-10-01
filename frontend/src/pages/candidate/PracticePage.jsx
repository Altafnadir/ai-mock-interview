import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  Play,
  Target,
  RefreshCw,
  AlertCircle,
  Clock,
  BookOpen,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';
import { practiceApi } from '../../api/practice';

export default function PracticePage() {
  const [drills, setDrills] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedQuestions, setExpandedQuestions] = useState({});

  useEffect(() => {
    fetchDrills();
  }, []);

  const fetchDrills = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await practiceApi.getDrills();
      setDrills(response.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load practice recommendations. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleQuestions = (drillId) => {
    setExpandedQuestions((prev) => ({
      ...prev,
      [drillId]: !prev[drillId],
    }));
  };

  if (isLoading) {
    return <Loader text="Loading your personalized practice recommendations..." size="lg" />;
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-12">
        <Card className="border-red-200 dark:border-red-900/50 p-6 text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
            Unable to Load Practice Drills
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">{error}</p>
          <Button icon={RefreshCw} onClick={fetchDrills} variant="primary">
            Retry Connection
          </Button>
        </Card>
      </div>
    );
  }

  if (drills.length === 0) {
    return (
      <div className="max-w-2xl mx-auto mt-12">
        <Card className="p-8 text-center border-dashed border-slate-300 dark:border-slate-700">
          <Target className="w-12 h-12 text-slate-400 mx-auto mb-4" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
            No Practice Drills Available
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
            Complete your first mock interview to unlock AI-personalized drills targeting your growth areas.
          </p>
          <Link to="/interview/setup">
            <Button icon={Play} variant="primary">
              Start an Interview
            </Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            Interactive Practice Recommendations
            <Sparkles className="w-5 h-5 text-amber-500 fill-amber-500/20" />
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Targeted micro-drills engineered from your recent evaluation reports and speech metrics.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          icon={RefreshCw}
          onClick={fetchDrills}
          title="Refresh recommendations"
        >
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {drills.map((drill, idx) => {
          const drillId = drill.id || `drill-${idx}`;
          const isPersonalized = !!drill.is_personalized;
          const questions = drill.suggested_questions || [];
          const hasQuestions = questions.length > 0;
          const showQuestions = !!expandedQuestions[drillId];

          const setupUrl = `/interview/setup?topic=${encodeURIComponent(
            drill.suggested_topic || drill.title
          )}&role=${encodeURIComponent(drill.suggested_role || '')}&category=${encodeURIComponent(
            drill.suggested_category || ''
          )}`;

          return (
            <Card
              key={drillId}
              hoverEffect
              className="border-slate-200 dark:border-slate-800 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant="primary" size="sm">
                      {drill.category || 'Practice'}
                    </Badge>
                    {isPersonalized && (
                      <Badge variant="success" size="sm" className="flex items-center gap-1">
                        <Sparkles className="w-3 h-3" />
                        Personalized
                      </Badge>
                    )}
                  </div>
                  <span className="text-xs text-slate-500 dark:text-slate-400 font-mono flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {drill.duration}
                  </span>
                </div>

                <div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-white">
                    {drill.title}
                  </h3>
                  {drill.score_context && (
                    <span className="inline-block mt-1 text-[11px] font-semibold px-2 py-0.5 rounded bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                      {drill.score_context}
                    </span>
                  )}
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  {drill.desc}
                </p>

                {hasQuestions && (
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/60">
                    <button
                      type="button"
                      onClick={() => toggleQuestions(drillId)}
                      className="text-xs font-semibold text-primary-600 dark:text-primary-400 hover:text-primary-700 flex items-center gap-1"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      {showQuestions ? 'Hide sample questions' : `View ${questions.length} suggested questions`}
                      {showQuestions ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>

                    {showQuestions && (
                      <ul className="mt-2 space-y-1.5 pl-2 text-xs text-slate-600 dark:text-slate-300">
                        {questions.map((q, qIdx) => (
                          <li key={qIdx} className="list-disc ml-3">
                            {q}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-slate-400 font-medium">Focus: {drill.tag}</span>
                <Link to={setupUrl}>
                  <Button size="sm" icon={Play} variant="primary">
                    Practice this &rarr;
                  </Button>
                </Link>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
