import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, RotateCcw, Volume2, VolumeX } from 'lucide-react';

export default function WaveformPlayer({
  audioSrc,
  duration = 45, // default duration in seconds if not loaded
  bars = 40,
  className = '',
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef(null);

  // Generate deterministic bar heights for consistent waveform aesthetic
  const barHeights = React.useMemo(() => {
    return Array.from({ length: bars }, (_, i) => {
      const sinVal = Math.sin((i / bars) * Math.PI * 4);
      const cosVal = Math.cos((i / bars) * Math.PI * 2);
      return Math.max(15, Math.min(95, Math.round(35 + sinVal * 25 + cosVal * 20 + ((i % 5) * 6))));
    });
  }, [bars]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().catch(() => {});
      setIsPlaying(true);
    }
  };

  const handleSeek = (idx) => {
    if (!audioRef.current) return;
    const targetTime = (idx / bars) * (audioRef.current.duration || duration);
    audioRef.current.currentTime = targetTime;
    setCurrentTime(targetTime);
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const totalDuration = audioRef.current?.duration || duration;
  const progressRatio = totalDuration > 0 ? currentTime / totalDuration : 0;

  return (
    <div className={`p-4 rounded-2xl bg-slate-50 dark:bg-slate-850/60 border border-slate-200/80 dark:border-slate-800 ${className}`}>
      {audioSrc && <audio ref={audioRef} src={audioSrc} preload="metadata" />}

      <div className="flex items-center gap-4">
        {/* Play/Pause Button */}
        <button
          type="button"
          onClick={togglePlay}
          className="w-10 h-10 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center shadow-sm shrink-0 transition-transform active:scale-95"
          aria-label={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current ml-0.5" />}
        </button>

        {/* Waveform Bars */}
        <div className="flex-1 flex items-center justify-between gap-[3px] h-12 cursor-pointer select-none">
          {barHeights.map((h, i) => {
            const barRatio = i / bars;
            const isPlayed = barRatio <= progressRatio;

            return (
              <div
                key={i}
                onClick={() => handleSeek(i)}
                className="flex-1 rounded-full transition-all duration-150 hover:opacity-80"
                style={{
                  height: `${h}%`,
                  backgroundColor: isPlayed ? '#4F46E5' : '#CBD5E1',
                }}
              />
            );
          })}
        </div>

        {/* Time Counter */}
        <div className="text-xs font-semibold text-slate-600 dark:text-slate-300 font-mono shrink-0">
          {formatTime(currentTime)} / {formatTime(totalDuration)}
        </div>
      </div>
    </div>
  );
}
