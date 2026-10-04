import React from 'react';
import { Link } from 'react-router-dom';
import {
  Video,
  Mic,
  Eye,
  Smile,
  FileCheck,
  TrendingUp,
  ArrowRight,
  Shield,
  Sparkles,
  CheckCircle2,
  Award,
} from 'lucide-react';
import Button from '../../components/common/Button';
import Logo from '../../components/common/Logo';
import ThemeSwitcher from '../../components/common/ThemeSwitcher';

export default function LandingPage() {
  const FEATURES = [
    {
      icon: Mic,
      title: 'Speech & Voice Analytics',
      desc: 'Powered by OpenAI Whisper and Librosa. Evaluates speaking rate (WPM), pitch stability, pause durations, and detects filler words like "um", "uh", and "like".',
    },
    {
      icon: Eye,
      title: 'Webcam Vision & Posture',
      desc: 'Utilizes MediaPipe FaceMesh & Pose. Tracks eye contact %, looking-away events, slouching detection, and head stability in real-time.',
    },
    {
      icon: Smile,
      title: 'Facial Emotion Recognition',
      desc: 'Deep affective modeling analyzing facial affect: confidence, nervousness, happiness, stress indicators, and genuine smile percentage.',
    },
    {
      icon: Sparkles,
      title: 'Gemini STAR Method Scoring',
      desc: 'Evaluates answers using Google Gemini LLM rubrics against expected industry keywords, technical accuracy, and Situation-Task-Action-Result structure.',
    },
    {
      icon: FileCheck,
      title: 'Grammar & Vocabulary Insights',
      desc: 'Identifies grammatical slips, evaluates lexical diversity (Type-Token Ratio), sentence structure sophistication, and pronunciation clarity.',
    },
    {
      icon: TrendingUp,
      title: 'Customized Learning Curricula',
      desc: 'Automatically maps performance weaknesses (<70 score) to curated YouTube tutorials, targeted practice drills, and dynamic follow-up mock questions.',
    },
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 selection:bg-primary-500/20 selection:text-primary-300">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-primary-900/60 via-indigo-900/40 to-primary-900/60 border-b border-primary-500/20 py-2 px-4 text-center text-xs text-primary-200">
        <span className="font-semibold text-white">Final Year Project:</span> PMAS-Arid Agriculture University (GIMS) &bull; Project ID: <span className="font-mono font-bold text-amber-400">GIMS-BSSE-F202206</span>
      </div>

      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 dark:border-slate-800/80 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Logo variant="full" size="md" to="/" responsive={true} />
          
          <nav className="hidden md:flex items-center gap-6 text-sm text-slate-600 dark:text-slate-300">
            <a href="#features" className="hover:text-primary-500 transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-primary-500 transition-colors">How It Works</a>
            <Link to="/resources" className="hover:text-primary-500 transition-colors">Resources</Link>
          </nav>

          <div className="flex items-center gap-3">
            <ThemeSwitcher />
            <Link to="/login">
              <Button variant="ghost" size="sm" className="text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white">
                Sign In
              </Button>
            </Link>
            <Link to="/register">
              <Button variant="primary" size="sm" className="font-semibold shadow-md shadow-primary-600/20">
                Get Started Free
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-32">
        {/* Background glow circles */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-1/3 left-1/4 w-72 h-72 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-xs font-semibold uppercase tracking-wider mb-8">
            <Award className="w-4 h-4 text-amber-400" />
            Next-Gen Multimodal Mock Interview Platform
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight max-w-4xl mx-auto leading-tight sm:leading-tight text-slate-900 dark:text-white">
            Walk into your next interview with{' '}
            <span className="bg-gradient-to-r from-primary-600 via-indigo-500 to-sky-500 dark:from-primary-400 dark:via-indigo-300 dark:to-sky-400 bg-clip-text text-transparent">
              genuine confidence
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Practice realistic questions tailored to your background, then get clear, supportive feedback on your answers, speaking rhythm, and presence — so you can shine when it counts.
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <Link to="/register">
              <Button size="lg" className="shadow-lg shadow-primary-600/30 font-semibold" icon={ArrowRight}>
                Start Free Mock Interview
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-900 text-slate-700 dark:text-slate-200">
                Sign In to Dashboard
              </Button>
            </Link>
            <Link to="/admin/login">
              <Button size="lg" variant="ghost" className="text-slate-500 dark:text-slate-400 hover:text-amber-500 dark:hover:text-amber-400" icon={Shield}>
                Admin Portal
              </Button>
            </Link>
          </div>

          {/* Quick Metrics Bar */}
          <div className="mt-16 pt-10 border-t border-slate-200/80 dark:border-slate-800/80 grid grid-cols-2 md:grid-cols-4 gap-6 text-center max-w-4xl mx-auto">
            <div>
              <div className="text-3xl font-extrabold text-slate-900 dark:text-white">120+</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 uppercase tracking-wide">Interview Questions</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-slate-900 dark:text-white">11 Roles</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 uppercase tracking-wide">Tech Job Tracks</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-slate-900 dark:text-white">6 AI Layers</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 uppercase tracking-wide">Speech, Vision, Content</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-slate-900 dark:text-white">Instant</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 uppercase tracking-wide">PDF & Video Reports</div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Grid */}
      <section className="py-20 bg-slate-100/60 dark:bg-slate-900/50 border-y border-slate-200/80 dark:border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-semibold text-primary-500 dark:text-primary-400 uppercase tracking-widest mb-2">
              Advanced Evaluation Engine
            </h2>
            <h3 className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white">
              Every Dimension of Your Performance Analyzed
            </h3>
            <p className="mt-4 text-slate-600 dark:text-slate-400 text-sm sm:text-base">
              Beyond simple text quizzes, our system assesses verbal, non-verbal, and technical competencies simultaneously.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {FEATURES.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <div
                  key={i}
                  className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-primary-500/40 shadow-sm transition-all duration-200 group"
                >
                  <div className="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-950 border border-primary-200 dark:border-primary-800/60 flex items-center justify-center text-primary-600 dark:text-primary-400 group-hover:scale-105 transition-transform mb-5">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h4 className="text-lg font-bold text-slate-900 dark:text-white mb-2">{feature.title}</h4>
                  <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{feature.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-xs font-semibold text-primary-500 dark:text-primary-400 uppercase tracking-widest mb-2">
          Simple 4-Step Process
        </h2>
        <h3 className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white mb-14">
          How The System Works
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm text-left">
            <span className="text-4xl font-extrabold text-primary-500">01</span>
            <h4 className="text-base font-bold text-slate-900 dark:text-white mt-4 mb-2">Upload Resume</h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Upload your PDF/DOCX resume. The AI parses your technical skills, projects, and detects skill gaps.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm text-left">
            <span className="text-4xl font-extrabold text-primary-500">02</span>
            <h4 className="text-base font-bold text-white mt-4 mb-2">Configure Mock Session</h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Select target role (Frontend, Backend, DevOps, ML), difficulty, category (Technical, HR, Behavioral), and test your webcam.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm text-left">
            <span className="text-4xl font-extrabold text-primary-500">03</span>
            <h4 className="text-base font-bold text-slate-900 dark:text-white mt-4 mb-2">Live Interview Room</h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Answer simulated interview questions with countdown timers, speech-to-speech audio, and dynamic follow-up queries.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-sm text-left">
            <span className="text-4xl font-extrabold text-primary-500">04</span>
            <h4 className="text-base font-bold text-slate-900 dark:text-white mt-4 mb-2">Instant Feedback & PDF</h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Review overall 0-100 scores, posture/emotion timelines, download official PDF reports, and watch recommended learning videos.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200/80 dark:border-slate-800/80 py-10 bg-slate-50 dark:bg-slate-950 text-slate-500 text-xs text-center">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-3 flex flex-col items-center">
          <Logo variant="full" size="sm" to="/" />
          <p className="font-semibold text-slate-600 dark:text-slate-400">
            Mock Interview AI &bull; AI-Based Mock Interview Preparation System (Project ID: GIMS-BSSE-F202206)
          </p>
          <p>
            Department of Software Engineering, PMAS-Arid Agriculture University (GIMS), Rawalpindi.
          </p>
          <div className="pt-2 flex justify-center gap-6 text-slate-500 dark:text-slate-400">
            <Link to="/login" className="hover:text-primary-500">Candidate Login</Link>
            <Link to="/register" className="hover:text-primary-500">Register</Link>
            <Link to="/admin/login" className="hover:text-amber-500">Admin Login</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
