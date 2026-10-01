import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Video,
  Mic,
  Camera,
  CheckCircle2,
  AlertCircle,
  Play,
  Settings,
  HelpCircle,
  Sparkles,
} from 'lucide-react';
import { interviewApi } from '../../api/interview';
import { resumeApi } from '../../api/resume';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';

export default function InterviewSetupPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const prefillTopic = searchParams.get('topic') || '';
  const prefillRole = searchParams.get('role') || '';
  const prefillCategory = searchParams.get('category') || '';
  const prefillDifficulty = searchParams.get('difficulty') || '';

  // Taxonomy & Resume state
  const [jobRoles, setJobRoles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [difficulties, setDifficulties] = useState([]);
  const [resumes, setResumes] = useState([]);

  // Form selections
  const [selectedRole, setSelectedRole] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedResume, setSelectedResume] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);

  // Hardware state
  const [mediaStream, setMediaStream] = useState(null);
  const [cameraOk, setCameraOk] = useState(false);
  const [micOk, setMicOk] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [isInitializing, setIsInitializing] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const videoRef = useRef(null);
  const audioContextRef = useRef(null);
  const animFrameRef = useRef(null);

  useEffect(() => {
    loadSetupData();
    checkPermissions();

    return () => {
      // Clean up webcam and audio listeners on leave
      if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, []);

  const loadSetupData = async () => {
    try {
      const [rRes, cRes, dRes, resRes] = await Promise.all([
        interviewApi.getJobRoles(),
        interviewApi.getCategories(),
        interviewApi.getDifficulties(),
        resumeApi.getResumes(),
      ]);

      setJobRoles(rRes.data);
      setCategories(cRes.data);
      setDifficulties(dRes.data);
      setResumes(resRes.data);

      const matchedRole = rRes.data.find(
        (r) => r.id === prefillRole || r.name.toLowerCase().includes((prefillRole || '').toLowerCase())
      );
      const matchedCat = cRes.data.find(
        (c) => c.id === prefillCategory || c.name.toLowerCase().includes((prefillCategory || '').toLowerCase())
      );
      const matchedDiff = dRes.data.find(
        (d) => d.id === prefillDifficulty || d.name.toLowerCase().includes((prefillDifficulty || '').toLowerCase())
      );

      setSelectedRole(matchedRole ? matchedRole.id : (rRes.data[0]?.id || ''));
      setSelectedCategory(matchedCat ? matchedCat.id : (cRes.data[0]?.id || ''));
      setSelectedDifficulty(matchedDiff ? matchedDiff.id : (dRes.data[0]?.id || ''));
      if (resRes.data.length > 0) setSelectedResume(resRes.data[0].id);
    } catch {
      // Seeded fallback options for local testing
      const fbRoles = [
        { id: 'r1', name: 'Frontend Developer' },
        { id: 'r2', name: 'Backend Developer' },
        { id: 'r3', name: 'Full Stack Developer' },
        { id: 'r4', name: 'Software Engineer' },
      ];
      const fbCats = [
        { id: 'c1', name: 'Technical' },
        { id: 'c2', name: 'HR' },
        { id: 'c3', name: 'Behavioral' },
        { id: 'c4', name: 'Mixed' },
      ];
      const fbDiffs = [
        { id: 'd1', name: 'Beginner' },
        { id: 'd2', name: 'Intermediate' },
        { id: 'd3', name: 'Advanced' },
      ];
      setJobRoles(fbRoles);
      setCategories(fbCats);
      setDifficulties(fbDiffs);

      const matchedRole = fbRoles.find(
        (r) => r.id === prefillRole || r.name.toLowerCase().includes((prefillRole || '').toLowerCase())
      );
      const matchedCat = fbCats.find(
        (c) => c.id === prefillCategory || c.name.toLowerCase().includes((prefillCategory || '').toLowerCase())
      );
      setSelectedRole(matchedRole ? matchedRole.id : 'r1');
      setSelectedCategory(matchedCat ? matchedCat.id : 'c4');
      setSelectedDifficulty('d1');
    } finally {
      setIsInitializing(false);
    }
  };

  const checkPermissions = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: true,
      });

      setMediaStream(stream);
      setCameraOk(true);
      setMicOk(true);

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Audio level meter
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      audioContextRef.current = audioCtx;
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);

      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      const updateAudio = () => {
        analyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
        }
        const avg = sum / dataArray.length;
        setAudioLevel(Math.min(100, Math.round((avg / 128) * 100)));
        animFrameRef.current = requestAnimationFrame(updateAudio);
      };
      updateAudio();
    } catch (err) {
      console.warn('Webcam/Mic permission denied or not available:', err);
      setCameraOk(false);
      setMicOk(false);
    }
  };

  const handleStartInterview = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const res = await interviewApi.createSession({
        job_role_id: selectedRole,
        category_id: selectedCategory,
        difficulty_id: selectedDifficulty,
        resume_id: selectedResume || null,
        num_questions: parseInt(numQuestions),
      });

      toast.success('Interview session created! Entering live room...');
      navigate(`/interview/${res.data.id}/room`);
    } catch (err) {
      // In offline/demo fallback mode, generate a mock session ID
      toast.info('Initializing live interview room...');
      navigate(`/interview/session-demo-01/room`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isInitializing) {
    return <Loader text="Configuring interview setup environment..." size="lg" />;
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          Configure Your Mock Interview
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Customize your interview environment, verify webcam & microphone, and launch.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Setup Form (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {prefillTopic && (
            <div className="bg-primary-50 dark:bg-primary-950/40 border border-primary-200 dark:border-primary-800 rounded-lg p-3.5 flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-primary-600 dark:text-primary-400 mt-0.5 shrink-0" />
              <div>
                <h4 className="text-xs font-bold text-primary-900 dark:text-primary-200">
                  Targeted Practice Drill Mode Active
                </h4>
                <p className="text-xs text-primary-700 dark:text-primary-300 mt-0.5">
                  Parameters have been pre-configured to target: <strong>{prefillTopic}</strong>.
                </p>
              </div>
            </div>
          )}
          <Card title="Interview Parameters" className="border-slate-200 dark:border-slate-800">
            <form onSubmit={handleStartInterview} className="space-y-4">
              {/* Job Role Selection */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                  Target Job Role
                </label>
                <select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-sm text-slate-900 dark:text-slate-100 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                >
                  {jobRoles.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Category & Difficulty */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                    Interview Category
                  </label>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-sm text-slate-900 dark:text-slate-100 focus:border-primary-500"
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name} ({c.name === 'Mixed' ? 'Recommended' : c.name})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                    Difficulty Level
                  </label>
                  <select
                    value={selectedDifficulty}
                    onChange={(e) => setSelectedDifficulty(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-sm text-slate-900 dark:text-slate-100 focus:border-primary-500"
                  >
                    {difficulties.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Resume Selection */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                  Tailor Against Resume
                </label>
                <select
                  value={selectedResume}
                  onChange={(e) => setSelectedResume(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-sm text-slate-900 dark:text-slate-100 focus:border-primary-500"
                >
                  <option value="">No Resume (General Questions Only)</option>
                  {resumes.map((res) => (
                    <option key={res.id} value={res.id}>
                      {res.original_filename} (Active)
                    </option>
                  ))}
                </select>
              </div>

              {/* Number of Questions Slider */}
              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                    Question Count
                  </label>
                  <span className="text-xs font-bold text-primary-500 font-mono">
                    {numQuestions} Questions (~{numQuestions * 2} mins)
                  </span>
                </div>
                <input
                  type="range"
                  min="3"
                  max="10"
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(e.target.value)}
                  className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
              </div>

              <div className="pt-4">
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  className="w-full font-bold shadow-lg shadow-primary-600/30"
                  isLoading={isSubmitting}
                  icon={Play}
                >
                  Start Live Video Interview
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Device Preview & Guidelines (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          <Card title="Hardware Check" className="border-slate-200 dark:border-slate-800">
            {/* Live Camera View */}
            <div className="relative aspect-video rounded-xl overflow-hidden bg-slate-950 border border-slate-800 flex items-center justify-center">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover transform -scale-x-100"
              />
              {!cameraOk && (
                <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center bg-slate-900/90 text-slate-400">
                  <Camera className="w-8 h-8 text-slate-500 mb-2" />
                  <p className="text-xs">Camera preview unavailable. Please grant webcam permissions.</p>
                </div>
              )}
            </div>

            {/* Hardware Status Indicators */}
            <div className="mt-4 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-slate-600 dark:text-slate-300 font-medium">
                  <Camera className="w-4 h-4 text-primary-500" />
                  Webcam Feed
                </span>
                <span className={`font-semibold flex items-center gap-1 ${cameraOk ? 'text-emerald-500' : 'text-rose-500'}`}>
                  {cameraOk ? <CheckCircle2 className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
                  {cameraOk ? 'Connected' : 'Permission Required'}
                </span>
              </div>

              {/* Audio Level Meter */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="flex items-center gap-2 text-slate-600 dark:text-slate-300 font-medium">
                    <Mic className="w-4 h-4 text-primary-500" />
                    Microphone Input
                  </span>
                  <span className={`font-semibold ${micOk ? 'text-emerald-500' : 'text-rose-500'}`}>
                    {micOk ? `${audioLevel}% Level` : 'Disconnected'}
                  </span>
                </div>
                <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 transition-all duration-75"
                    style={{ width: `${audioLevel}%` }}
                  />
                </div>
              </div>
            </div>
          </Card>

          {/* Quick Guidelines */}
          <Card title="Interview Instructions" className="border-slate-200 dark:border-slate-800">
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-primary-500 flex-shrink-0 mt-0.5" />
                <span>Keep your webcam positioned at eye-level to maximize eye contact score.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-primary-500 flex-shrink-0 mt-0.5" />
                <span>Speak into a quiet room with minimal background echo.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-primary-500 flex-shrink-0 mt-0.5" />
                <span>Utilize the STAR method (Situation, Task, Action, Result) for behavioral answers.</span>
              </li>
            </ul>
          </Card>
        </div>
      </div>
    </div>
  );
}
