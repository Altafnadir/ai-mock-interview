import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Play, Target, CheckCircle2, Video } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';

const DRILLS = [
  {
    title: 'Silent Pause Drill',
    tag: 'filler_words',
    duration: '5 Mins',
    desc: 'Answer a complex technical query without using "um", "uh", or "like". Replace every verbal hesitation with a calm 1-second silent breath.',
    category: 'Vocal Discipline',
  },
  {
    title: 'STAR Method Storytelling Drill',
    tag: 'star_method',
    duration: '8 Mins',
    desc: 'Structure a past bug resolution strictly dividing your answer into 15s Situation, 15s Task, 45s Action, and 15s quantifiable Result.',
    category: 'Behavioral',
  },
  {
    title: 'Webcam Eye-Level Gaze Lock',
    tag: 'eye_contact',
    duration: '4 Mins',
    desc: 'Focus continuously on the camera lens while answering technical questions to build unconscious gaze endurance.',
    category: 'Body Language',
  },
  {
    title: '60-Second System Design Elevator Pitch',
    tag: 'technical',
    duration: '6 Mins',
    desc: 'Explain how you would design a high-throughput URL shortener or rate limiter in under 60 seconds with clear trade-offs.',
    category: 'Technical Architecture',
  },
];

export default function PracticePage() {
  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          Interactive Practice Recommendations
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Targeted micro-drills designed to turn weak points into unshakeable interview habits.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {DRILLS.map((drill, idx) => (
          <Card
            key={idx}
            hoverEffect
            className="border-slate-200 dark:border-slate-800 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <Badge variant="primary" size="sm">
                  {drill.category}
                </Badge>
                <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                  {drill.duration}
                </span>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white mb-2">
                {drill.title}
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                {drill.desc}
              </p>
            </div>

            <div className="pt-6 mt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
              <span className="text-[11px] text-slate-400 font-medium">Focus: {drill.tag}</span>
              <Link to="/interview/setup">
                <Button size="sm" icon={Play}>
                  Start Drill &rarr;
                </Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
