import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  CheckCircle2,
  Loader2,
  Clock,
  Sparkles,
  ArrowRight,
  FileCheck2,
} from 'lucide-react';
import { interviewApi } from '../../api/interview';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';

const PIPELINE_STEPS = [
  { id: 'transcribing', name: 'Whisper Speech-to-Text Transcription', desc: 'Computing words-per-minute and detecting disfluencies' },
  { id: 'voice', name: 'Librosa Vocal & Tone DSP Analysis', desc: 'Measuring pitch variance, harmonic ratio, and hesitation pauses' },
  { id: 'vision', name: 'MediaPipe Eye-Contact & Posture Mesh', desc: 'Evaluating gaze stability, looking-away frequency, and slouching' },
  { id: 'emotion', name: 'Facial Emotion & Confidence Modeling', desc: 'Determining affective distribution (confidence, stress, smiling)' },
  { id: 'grammar', name: 'LanguageTool & Lexical Analysis', desc: 'Checking grammatical precision and vocabulary richness' },
  { id: 'content', name: 'Gemini LLM STAR Rubric Evaluation', desc: 'Assessing technical depth, domain keywords, and STAR answers' },
  { id: 'scoring', name: 'Weighted Scoring Matrix & Recommendations', desc: 'Aggregating 0-100 scores and mapping targeted learning videos' },
];

export default function ProcessingPage() {
  const { id: sessionId } = useParams();
  const navigate = useNavigate();

  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    // Poll status or simulate progression steps
    let step = 0;
    const interval = setInterval(async () => {
      try {
        const res = await interviewApi.getSessionStatus(sessionId);
        const st = res.data?.status;
        if (st === 'analyzed' || st === 'completed') {
          setIsCompleted(true);
          clearInterval(interval);
          setTimeout(() => {
            navigate(`/reports/${sessionId}`);
          }, 1500);
          return;
        }
      } catch (err) {
        // Local progression simulation
      }

      step += 1;
      if (step < PIPELINE_STEPS.length) {
        setCurrentStepIndex(step);
      } else {
        setIsCompleted(true);
        clearInterval(interval);
        setTimeout(() => {
          navigate(`/reports/${sessionId}`);
        }, 1500);
      }
    }, 1800);

    return () => clearInterval(interval);
  }, [sessionId, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      <div className="max-w-xl w-full text-center">
        <div className="w-16 h-16 rounded-2xl bg-primary-600/10 border border-primary-500/20 text-primary-400 flex items-center justify-center mx-auto mb-6 shadow-xl">
          <Sparkles className="w-8 h-8 animate-pulse text-primary-500 dark:text-primary-400" />
        </div>

        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Analyzing Your Mock Interview
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-2 max-w-md mx-auto">
          Our multimodal AI engine is currently processing your video and audio recording.
        </p>

        {/* Pipeline Step Checklist */}
        <Card className="mt-8 border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/90 text-left shadow-2xl">
          <div className="space-y-4">
            {PIPELINE_STEPS.map((step, idx) => {
              const isPast = idx < currentStepIndex || isCompleted;
              const isCurrent = idx === currentStepIndex && !isCompleted;
              const isFuture = idx > currentStepIndex && !isCompleted;

              return (
                <div key={step.id} className="flex items-start gap-3.5">
                  <div className="mt-0.5 flex-shrink-0">
                    {isPast ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                    ) : isCurrent ? (
                      <Loader2 className="w-5 h-5 text-primary-400 animate-spin" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border border-slate-700 bg-slate-800/40" />
                    )}
                  </div>
                  <div className="flex-1">
                    <p
                      className={`text-sm font-semibold transition-colors ${
                        isPast
                          ? 'text-slate-200'
                          : isCurrent
                          ? 'text-primary-400 font-bold'
                          : 'text-slate-500'
                      }`}
                    >
                      {step.name}
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {step.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {isCompleted && (
            <div className="mt-6 pt-6 border-t border-slate-800 text-center">
              <Button
                variant="primary"
                size="lg"
                onClick={() => navigate(`/reports/${sessionId}`)}
                icon={FileCheck2}
                className="w-full font-bold shadow-lg shadow-primary-600/30"
              >
                View Complete Performance Report &rarr;
              </Button>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
