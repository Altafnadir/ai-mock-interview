import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Video,
  Mic,
  Eye,
  Smile,
  FileCheck,
  TrendingUp,
  ArrowRight,
  Play,
  CheckCircle2,
  X,
  Sparkles,
  Shield,
  Layers,
  Award,
} from 'lucide-react';
import Logo from '../../components/common/Logo';
import ThemeSwitcher from '../../components/common/ThemeSwitcher';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';
import Modal from '../../components/ui/Modal';

export default function LandingPage() {
  const [showDemoModal, setShowDemoModal] = useState(false);

  const features = [
    {
      icon: FileCheck,
      title: 'Resume & Skill Gap Analysis',
      desc: 'Upload PDF/DOCX resumes to extract technical competencies, calculate benchmark fit, and identify missing prerequisites.',
    },
    {
      icon: Sparkles,
      title: 'AI Question Generator',
      desc: 'Dynamic questions tailored to role, seniority, and category (Technical, HR, Behavioral) with real-time follow-ups.',
    },
    {
      icon: Mic,
      title: 'Speech & Audio Metrics',
      desc: 'Analyzes volume stability, pitch variance, speaking pace (WPM), pronunciation clarity, and filler words (um, uh, like).',
    },
    {
      icon: Eye,
      title: 'Computer Vision & Posture',
      desc: 'Local MediaPipe tracking for gaze consistency, blink rate, head tilt, shoulder alignment, and looking-away events.',
    },
    {
      icon: Smile,
      title: 'Facial Emotion Recognition',
      desc: 'Real-time emotion distribution timelines measuring confidence, nervousness, neutral composure, and genuine smiles.',
    },
    {
      icon: TrendingUp,
      title: 'Comprehensive Actionable Reports',
      desc: 'Multi-dimensional radar scores, STAR methodology feedback, and direct links to curated video lessons for weak areas.',
    },
  ];

  const steps = [
    {
      num: '01',
      title: 'Upload Resume or Pick Role',
      desc: 'Choose from 11 specialized software tracks or let the parser extract your skills directly from your resume.',
    },
    {
      num: '02',
      title: 'Configure Interview & Tech Check',
      desc: 'Select difficulty, question count, and verify camera, microphone, and lighting with live feedback.',
    },
    {
      num: '03',
      title: 'Practice with Real-Time AI',
      desc: 'Answer realistic timed questions with live gaze and volume estimators, or dynamic follow-up prompts.',
    },
    {
      num: '04',
      title: 'Review Insights & AI Coaching',
      desc: 'Download 3 tailored PDF reports, review speech transcripts, and ask the AI Coach targeted questions.',
    },
  ];

  return (
    <div className="min-h-screen bg-[#F5F7FB] dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans antialiased selection:bg-indigo-500/20 selection:text-indigo-600">
      {/* Top Banner (Truthful FYP attribution) */}
      <div className="bg-[#0B1437] text-white text-xs py-2 px-4 text-center border-b border-indigo-900/50 flex items-center justify-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        <span className="font-medium text-slate-300">
          Final-Year Project · GIMS, PMAS-Arid Agriculture University (Project ID: GIMS-BSSE-F202206)
        </span>
      </div>

      {/* Navigation Bar */}
      <header className="sticky top-0 z-40 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
          <Logo variant="full" size="md" />

          {/* Center Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 dark:text-slate-300">
            <a href="#features" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              How It Works
            </a>
            <Link to="/login" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Resources
            </Link>
          </nav>

          {/* Right Action Buttons */}
          <div className="flex items-center gap-3">
            <ThemeSwitcher />
            <Link
              to="/login"
              className="text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 px-3 py-2 transition-colors"
            >
              Log In
            </Link>
            <Link to="/register">
              <Button variant="primary" size="md" className="font-semibold shadow-xs">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section (Matching Panel 1: 01_landing.png) */}
      <section className="relative pt-12 pb-20 lg:pt-20 lg:pb-28 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
            
            {/* Left Hero Column */}
            <div className="lg:col-span-6 space-y-6 text-left">
              {/* Badge Pill */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200/80 dark:border-indigo-800 text-indigo-600 dark:text-indigo-400 text-xs font-semibold tracking-wide">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 dark:bg-indigo-400" />
                NEW · AI-Powered Interview Preparation
              </div>

              {/* Main Headline */}
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 dark:text-white tracking-tight leading-[1.15]">
                Ace Every Interview with{' '}
                <span className="text-indigo-600 dark:text-indigo-400">
                  AI Confidence
                </span>
              </h1>

              {/* Subtitle */}
              <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 leading-relaxed max-w-xl">
                Practice real interviews, get AI feedback, improve your communication, confidence and performance.
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link to="/register">
                  <Button variant="primary" size="lg" className="font-semibold shadow-md shadow-indigo-600/25">
                    Start Free Interview
                  </Button>
                </Link>
                <Button
                  variant="secondary"
                  size="lg"
                  onClick={() => setShowDemoModal(true)}
                  icon={Play}
                  className="font-semibold bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 hover:bg-slate-50 text-slate-800 dark:text-slate-200"
                >
                  Watch Demo
                </Button>
              </div>

              {/* Truthful Trust Badge */}
              <div className="pt-6 flex items-center gap-4">
                <div className="flex -space-x-2">
                  <div className="w-9 h-9 rounded-full ring-2 ring-white dark:ring-slate-950 bg-indigo-500 text-white flex items-center justify-center text-xs font-bold">
                    HT
                  </div>
                  <div className="w-9 h-9 rounded-full ring-2 ring-white dark:ring-slate-950 bg-emerald-500 text-white flex items-center justify-center text-xs font-bold">
                    AN
                  </div>
                  <div className="w-9 h-9 rounded-full ring-2 ring-white dark:ring-slate-950 bg-amber-500 text-white flex items-center justify-center text-xs font-bold">
                    SA
                  </div>
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                    Built for University Candidates & Job Seekers
                  </p>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Department of Computer Science · GIMS, PMAS-AAUR
                  </p>
                </div>
              </div>
            </div>

            {/* Right Hero Column (Exact Composite Mockup Card) */}
            <div className="lg:col-span-6 relative flex justify-center lg:justify-end">
              {/* Outer Laptop / Terminal Screen Container */}
              <div className="relative w-full max-w-lg bg-[#0F172A] rounded-2xl p-3 shadow-2xl border border-slate-700/60 overflow-hidden">
                {/* Simulated Webcam View */}
                <div className="relative w-full aspect-video rounded-xl bg-slate-900 overflow-hidden flex flex-col justify-between p-4">
                  {/* Background Video Illustration / Avatar */}
                  <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
                    <div className="w-28 h-28 rounded-full bg-gradient-to-tr from-indigo-500 to-sky-400 p-1">
                      <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center text-white text-3xl font-black">
                        AI
                      </div>
                    </div>
                  </div>

                  {/* Top Overlay Badge */}
                  <div className="relative z-10 flex items-center justify-between">
                    <span className="px-2.5 py-1 rounded-full bg-rose-500/90 text-white text-[10px] font-bold flex items-center gap-1.5 shadow-sm">
                      <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
                      Recording
                    </span>
                    <span className="px-2.5 py-1 rounded-md bg-black/60 text-slate-300 text-[10px] font-mono backdrop-blur-sm">
                      04:12
                    </span>
                  </div>

                  {/* Bottom Control Bar */}
                  <div className="relative z-10 flex items-center justify-center gap-3 py-1">
                    <div className="w-8 h-8 rounded-full bg-slate-800/90 text-white flex items-center justify-center text-xs shadow-sm">
                      <Mic className="w-4 h-4" />
                    </div>
                    <div className="w-8 h-8 rounded-full bg-slate-800/90 text-white flex items-center justify-center text-xs shadow-sm">
                      <Video className="w-4 h-4" />
                    </div>
                    <div className="w-8 h-8 rounded-full bg-rose-600 text-white flex items-center justify-center text-xs shadow-sm">
                      <X className="w-4 h-4" />
                    </div>
                  </div>
                </div>

                {/* Floating Card 1: Sample AI Score Card (Matches 01_landing.png) */}
                <div className="absolute top-6 left-2 sm:-left-4 z-20 w-48 sm:w-52 bg-white dark:bg-slate-900 rounded-2xl p-4 shadow-xl border border-slate-200/90 dark:border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                      Sample Report
                    </span>
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                  </div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">
                      89%
                    </span>
                    <Badge variant="success" size="sm">Very Good</Badge>
                  </div>

                  {/* Sub-metrics checklist */}
                  <div className="mt-3 space-y-1.5 text-[11px] font-medium text-slate-600 dark:text-slate-300">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      <span>Confidence</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      <span>Communication</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      <span>Grammar</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      <span>Body Language</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      <span>Voice Quality</span>
                    </div>
                  </div>
                </div>

                {/* Floating Card 2: Performance Trend Sparkline */}
                <div className="absolute -bottom-4 right-2 sm:right-6 z-20 w-52 bg-white dark:bg-slate-900 rounded-2xl p-3.5 shadow-xl border border-slate-200/90 dark:border-slate-800">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="font-semibold text-slate-700 dark:text-slate-300">
                      Performance Trend
                    </span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold text-[10px]">
                      +15% this week
                    </span>
                  </div>
                  {/* SVG Sparkline */}
                  <div className="h-10 w-full pt-1">
                    <svg viewBox="0 0 100 30" className="w-full h-full overflow-visible">
                      <defs>
                        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.3" />
                          <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.0" />
                        </linearGradient>
                      </defs>
                      <path
                        d="M0 22 L16 18 L32 25 L48 15 L64 19 L80 12 L100 6 L100 30 L0 30 Z"
                        fill="url(#sparkGrad)"
                      />
                      <path
                        d="M0 22 L16 18 L32 25 L48 15 L64 19 L80 12 L100 6"
                        fill="none"
                        stroke="#4F46E5"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <circle cx="100" cy="6" r="3" fill="#4F46E5" />
                    </svg>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Features Grid Section */}
      <section id="features" className="py-20 bg-white dark:bg-slate-900 border-y border-slate-200/80 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-widest">
              Core Capabilities
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white mt-2">
              Everything You Need to Succeed
            </h2>
            <p className="mt-3 text-sm sm:text-base text-slate-500 dark:text-slate-400">
              Rigorous, automated multimodal assessment covering verbal clarity, facial composure, and technical answers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div
                  key={idx}
                  className="bg-[#F5F7FB] dark:bg-slate-800/60 border border-slate-200/70 dark:border-slate-700/60 rounded-2xl p-6 hover:border-indigo-400/50 hover:shadow-md transition-all duration-200"
                >
                  <div className="w-11 h-11 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200/80 dark:border-indigo-800 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mb-4">
                    <Icon className="w-5 h-5 stroke-[2.2]" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works (4 Steps) */}
      <section id="how-it-works" className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-widest">
            Simple Workflow
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white mt-2">
            How The System Works
          </h2>
          <p className="mt-3 text-sm sm:text-base text-slate-500 dark:text-slate-400">
            From resume upload to full AI performance debriefing in four straightforward stages.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, idx) => (
            <div
              key={idx}
              className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 relative shadow-xs"
            >
              <div className="text-3xl font-black text-indigo-600/30 dark:text-indigo-400/30 mb-2 font-mono">
                {step.num}
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 mb-2">
                {step.title}
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-16 bg-[#0B1437] text-white text-center relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-6">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            Ready to Ace Your Next Tech Interview?
          </h2>
          <p className="text-sm sm:text-base text-slate-300 max-w-xl mx-auto leading-relaxed">
            Get instant feedback on speech tempo, eye contact, and technical answer precision. 100% free for students and developers.
          </p>
          <div className="pt-2 flex justify-center gap-4">
            <Link to="/register">
              <Button variant="primary" size="lg" className="font-semibold shadow-lg shadow-indigo-600/30">
                Start Free Interview
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-10 text-xs text-slate-500 dark:text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <Logo variant="full" size="sm" />
          <p className="text-center">
            © {new Date().getFullYear()} Mock Interview AI · Built as a Final-Year Project at GIMS, PMAS-Arid Agriculture University.
          </p>
          <div className="flex gap-4">
            <Link to="/login" className="hover:text-slate-700 dark:hover:text-slate-200">
              Sign In
            </Link>
            <Link to="/admin/login" className="hover:text-slate-700 dark:hover:text-slate-200">
              Admin Portal
            </Link>
          </div>
        </div>
      </footer>

      {/* Watch Demo Modal */}
      <Modal
        isOpen={showDemoModal}
        onClose={() => setShowDemoModal(false)}
        title="Mock Interview AI Walkthrough"
        size="lg"
      >
        <div className="space-y-4">
          <div className="aspect-video bg-slate-900 rounded-xl overflow-hidden flex items-center justify-center text-white relative">
            <div className="text-center p-6 space-y-3">
              <div className="w-14 h-14 rounded-2xl bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-400 mx-auto">
                <Play className="w-7 h-7 fill-current ml-1" />
              </div>
              <h4 className="text-base font-bold">Interactive Platform Walkthrough</h4>
              <p className="text-xs text-slate-400 max-w-md">
                Experience multimodal speech and vision analytics, STAR-framework answer evaluations, and personalized AI coaching drills.
              </p>
            </div>
          </div>
          <div className="flex justify-end pt-2">
            <Link to="/register" onClick={() => setShowDemoModal(false)}>
              <Button variant="primary" size="md">
                Try It Live Free &rarr;
              </Button>
            </Link>
          </div>
        </div>
      </Modal>
    </div>
  );
}
