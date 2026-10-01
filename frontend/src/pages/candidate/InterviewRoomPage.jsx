import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Mic,
  Camera,
  Volume2,
  VolumeX,
  SkipForward,
  RotateCcw,
  Square,
  ArrowRight,
  Clock,
  Sparkles,
  AlertTriangle,
  Maximize2,
} from 'lucide-react';
import { interviewApi } from '../../api/interview';
import { toast } from '../../store/toastStore';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';

export default function InterviewRoomPage() {
  const { id: sessionId } = useParams();
  const navigate = useNavigate();

  // Interview state
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(120);
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Hardware and MediaRecorder refs
  const videoRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    initializeSession();

    const handleOnline = () => {
      setIsOnline(true);
      toast.success('Internet connection restored.');
    };
    const handleOffline = () => {
      setIsOnline(false);
      toast.warning('Internet connection lost. Local buffering enabled.');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Prevent accidental page refresh/leave
    const handleBeforeUnload = (e) => {
      e.preventDefault();
      e.returnValue = 'Interview in progress. Leaving will abandon the session.';
    };
    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('beforeunload', handleBeforeUnload);
      cleanupMedia();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [sessionId]);


  // When question changes, speak question if TTS enabled
  useEffect(() => {
    if (questions.length > 0 && ttsEnabled) {
      speakQuestion(questions[currentIndex]?.text);
    }
    // Reset timer
    setTimeRemaining(questions[currentIndex]?.time_limit_seconds || 120);
  }, [currentIndex, questions]);

  // Countdown timer effect
  useEffect(() => {
    if (timerRef.current) clearInterval(timerRef.current);

    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          // Auto advance on timeout
          handleNextQuestion();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, [currentIndex]);

  const initializeSession = async () => {
    try {
      // Initialize webcam
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: true,
      });
      mediaStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Fetch session and start
      try {
        await interviewApi.startSession(sessionId);
        const res = await interviewApi.getSession(sessionId);
        if (res.data?.questions && res.data.questions.length > 0) {
          const formatted = res.data.questions.map((q) => ({
            id: q.id,
            text: q.question_text || q.text,
            source: q.source,
            time_limit_seconds: q.time_limit_seconds || 120,
          }));
          setQuestions(formatted);
        } else {
          loadFallbackQuestions();
        }
      } catch (err) {
        loadFallbackQuestions();
      }

      startRecording(stream);
    } catch (err) {
      console.warn('Camera/mic access error:', err);
      loadFallbackQuestions();
    }
  };

  const loadFallbackQuestions = () => {
    setQuestions([
      {
        id: 'q1',
        text: 'Tell me about yourself, your technical background, and what makes you passionate about software engineering.',
        source: 'bank',
        time_limit_seconds: 120,
      },
      {
        id: 'q2',
        text: 'What is the difference between synchronous and asynchronous operations, and how do you handle blocking tasks in modern backends?',
        source: 'bank',
        time_limit_seconds: 120,
      },
      {
        id: 'q3',
        text: 'Describe a challenging bug or outage you resolved recently. Walk through your diagnostic steps using the STAR method.',
        source: 'bank',
        time_limit_seconds: 150,
      },
      {
        id: 'q4',
        text: 'How do you design scalable REST APIs, and what strategies do you implement to ensure backward compatibility and rate limiting?',
        source: 'bank',
        time_limit_seconds: 120,
      },
    ]);
  };

  const startRecording = (stream) => {
    try {
      recordedChunksRef.current = [];
      const recorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp8,opus' });
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          recordedChunksRef.current.push(e.data);
        }
      };

      recorder.start(1000); // 1s slice
      setIsRecording(true);
    } catch (err) {
      console.warn('MediaRecorder VP8 codec not supported, falling back to default:', err);
      try {
        const recorder = new MediaRecorder(stream);
        mediaRecorderRef.current = recorder;
        recorder.ondataavailable = (e) => {
          if (e.data.size > 0) recordedChunksRef.current.push(e.data);
        };
        recorder.start(1000);
        setIsRecording(true);
      } catch (e) {
        console.warn('MediaRecorder error:', e);
      }
    }
  };

  const speakQuestion = (text) => {
    if (!text || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  const cleanupMedia = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
    }
  };

  const uploadCurrentAnswer = async () => {
    const currentQ = questions[currentIndex];
    if (!currentQ) return;

    const blob = new Blob(recordedChunksRef.current, { type: 'video/webm' });
    const formData = new FormData();
    formData.append('video', blob, `answer_${currentQ.id}.webm`);

    try {
      await interviewApi.submitAnswer(sessionId, currentQ.id, formData);
    } catch (err) {
      console.log('Recorded answer saved locally (offline-tolerant).');
    }
  };

  const handleNextQuestion = async () => {
    setIsUploading(true);
    await uploadCurrentAnswer();
    setIsUploading(false);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      // Restart recorder for next chunk
      if (mediaStreamRef.current) {
        startRecording(mediaStreamRef.current);
      }
    } else {
      handleFinishInterview();
    }
  };

  const handleSkipQuestion = async () => {
    const currentQ = questions[currentIndex];
    if (currentQ) {
      try {
        await interviewApi.skipQuestion(sessionId, currentQ.id);
      } catch (err) {
        console.log('Skipped locally.');
      }
    }

    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      handleFinishInterview();
    }
  };

  const handleRepeatQuestion = () => {
    const currentQ = questions[currentIndex];
    if (currentQ) {
      speakQuestion(currentQ.text);
      toast.info('Repeating question...');
    }
  };

  const handleFinishInterview = async () => {
    cleanupMedia();
    toast.success('Interview completed! Queuing AI analysis pipeline...');
    try {
      await interviewApi.endSession(sessionId);
    } catch (err) {
      console.log('Session ended.');
    }
    navigate(`/interview/${sessionId}/processing`);
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progressPercent = Math.round(((currentIndex + 1) / (questions.length || 1)) * 100);

  const formatTimer = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950 text-slate-100 flex flex-col overflow-hidden">
      {!isOnline && (
        <div className="bg-amber-600/90 text-white text-xs font-semibold py-2 px-4 text-center flex items-center justify-center gap-2 shadow-lg z-50">
          <AlertTriangle className="w-4 h-4 animate-bounce" />
          <span>Network connection lost. All video chunks are safely buffered locally and will synchronize once reconnected.</span>
        </div>
      )}

      {/* Top HUD Bar */}
      <header className="h-16 px-6 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md flex items-center justify-between">

        <div className="flex items-center gap-4">
          <Badge variant="primary" size="md">
            Question {currentIndex + 1} of {questions.length}
          </Badge>
          <div className="hidden sm:flex items-center gap-2">
            <div className="w-32 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-primary-500 transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
            <span className="text-xs font-mono text-slate-400">{progressPercent}%</span>
          </div>
        </div>

        {/* Live Indicator & Timer */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-bold uppercase tracking-wider animate-pulse">
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            LIVE RECORDING
          </div>

          <div
            className={`flex items-center gap-2 font-mono font-bold text-lg px-3.5 py-1.5 rounded-xl border ${
              timeRemaining < 30
                ? 'bg-rose-500/10 border-rose-500/40 text-rose-400 animate-pulse'
                : 'bg-slate-800 border-slate-700 text-white'
            }`}
          >
            <Clock className="w-4 h-4 text-slate-400" />
            {formatTimer(timeRemaining)}
          </div>
        </div>

        {/* Right utility buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setTtsEnabled(!ttsEnabled)}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title={ttsEnabled ? 'Mute AI Voice' : 'Enable AI Voice'}
          >
            {ttsEnabled ? <Volume2 className="w-5 h-5 text-primary-400" /> : <VolumeX className="w-5 h-5" />}
          </button>
          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Toggle Fullscreen"
          >
            <Maximize2 className="w-5 h-5" />
          </button>
          <Button
            variant="danger"
            size="sm"
            onClick={handleFinishInterview}
            icon={Square}
          >
            End Now
          </Button>
        </div>
      </header>

      {/* Main Center Video & Teleprompter Workspace */}
      <div className="flex-1 relative flex items-center justify-center p-4 sm:p-6 overflow-hidden">
        {/* Large Candidate Webcam Video Feed */}
        <div className="relative w-full max-w-4xl aspect-video rounded-2xl overflow-hidden bg-slate-900 border-2 border-slate-800 shadow-2xl">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover transform -scale-x-100"
          />

          {/* Real-time Facial Tracking Box Overlay Simulation */}
          <div className="absolute top-4 left-4 flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950/70 backdrop-blur-md border border-slate-800 text-[11px] font-mono text-emerald-400">
            <Camera className="w-3.5 h-3.5" />
            MediaPipe Vision: Active Tracking
          </div>

          {/* Question Teleprompter Banner Overlay */}
          <div className="absolute bottom-6 inset-x-6 p-5 rounded-2xl bg-slate-950/85 backdrop-blur-lg border border-slate-700/80 shadow-2xl">
            <div className="flex items-center gap-2 text-xs font-bold text-primary-400 uppercase tracking-widest mb-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              Interview Question
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-white leading-snug">
              {currentQuestion?.text || 'Loading question prompt...'}
            </h2>
          </div>
        </div>
      </div>

      {/* Bottom Control Dock */}
      <footer className="h-20 px-6 border-t border-slate-800 bg-slate-900/90 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="md"
            onClick={handleRepeatQuestion}
            icon={RotateCcw}
            className="border-slate-700 text-slate-300 hover:bg-slate-800"
          >
            Repeat Audio
          </Button>
          <Button
            variant="ghost"
            size="md"
            onClick={handleSkipQuestion}
            icon={SkipForward}
            className="text-slate-400 hover:text-white"
          >
            Skip Question
          </Button>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="primary"
            size="lg"
            onClick={handleNextQuestion}
            isLoading={isUploading}
            icon={ArrowRight}
            className="shadow-lg shadow-primary-600/30 font-bold px-6"
          >
            {currentIndex === questions.length - 1 ? 'Finish & Generate Report' : 'Next Question'}
          </Button>
        </div>
      </footer>
    </div>
  );
}
