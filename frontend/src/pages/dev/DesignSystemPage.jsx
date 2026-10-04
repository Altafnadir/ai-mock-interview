import React, { useState } from 'react';
import Button from '../../components/ui/Button';
import Card, { CardHeader, CardTitle, CardDescription } from '../../components/ui/Card';
import StatCard from '../../components/ui/StatCard';
import ScoreRing from '../../components/ui/ScoreRing';
import ProgressBar from '../../components/ui/ProgressBar';
import Badge from '../../components/ui/Badge';
import Table from '../../components/ui/Table';
import Tabs from '../../components/ui/Tabs';
import Stepper from '../../components/ui/Stepper';
import Toggle from '../../components/ui/Toggle';
import Select from '../../components/ui/Select';
import RadioPills from '../../components/ui/RadioPills';
import Modal from '../../components/ui/Modal';
import Dropdown, { DropdownItem, DropdownDivider } from '../../components/ui/Dropdown';
import Avatar from '../../components/ui/Avatar';
import Skeleton from '../../components/ui/Skeleton';
import EmptyState from '../../components/ui/EmptyState';
import WaveformPlayer from '../../components/ui/WaveformPlayer';
import VideoCard from '../../components/ui/VideoCard';
import ChatBubble from '../../components/ui/ChatBubble';
import BadgeCard from '../../components/ui/BadgeCard';
import CalendarGrid from '../../components/ui/CalendarGrid';
import ThemeSwitcher from '../../components/common/ThemeSwitcher';
import { Eye, Flame, Shield, Award, Zap, Sparkles, MessageSquare, Play } from 'lucide-react';

export default function DesignSystemPage() {
  const [activeTab, setActiveTab] = useState('buttons');
  const [currentStep, setCurrentStep] = useState(1);
  const [toggleVal, setToggleVal] = useState(true);
  const [selectVal, setSelectVal] = useState('react');
  const [radioVal, setRadioVal] = useState('technical');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const tableColumns = [
    { header: 'Interview', key: 'role', render: (r) => <span className="font-semibold">{r.role}</span> },
    { header: 'Type', key: 'type', render: (r) => <Badge variant="neutral" size="sm">{r.type}</Badge> },
    { header: 'Score', key: 'score', render: (r) => <span className="font-bold text-emerald-600">{r.score}%</span> },
    { header: 'Date', key: 'date' },
    { header: 'Action', key: 'action', render: () => <span className="text-indigo-600 font-medium cursor-pointer hover:underline">View Report</span> },
  ];

  const tableData = [
    { id: 1, role: 'Frontend Developer', type: 'Technical', score: 89, date: 'May 12, 2024' },
    { id: 2, role: 'HR Assessment', type: 'HR', score: 84, date: 'May 10, 2024' },
    { id: 3, role: 'Backend Engineer', type: 'Technical', score: 78, date: 'May 05, 2024' },
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 p-6 sm:p-10">
      {/* Top Header */}
      <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between pb-8 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Design System & Component Showcase</h1>
          <p className="text-sm text-slate-500 mt-1">
            Standardized UI tokens, components, and responsive widgets across all 4 themes.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <ThemeSwitcher />
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            Open Demo Modal
          </Button>
        </div>
      </div>

      <div className="max-w-6xl mx-auto py-8 space-y-12">
        {/* Section 1: Buttons */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">1. Buttons & Variants</h2>
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="primary" size="sm">Primary SM</Button>
            <Button variant="primary" size="md">Primary MD</Button>
            <Button variant="primary" size="lg">Primary LG</Button>
            <Button variant="secondary" size="md">Secondary</Button>
            <Button variant="ghost" size="md">Ghost</Button>
            <Button variant="danger" size="md">Danger</Button>
            <Button variant="outline" size="md">Outline</Button>
            <Button variant="primary" size="md" loading>Loading</Button>
            <Button variant="primary" size="md" icon={Sparkles}>With Icon</Button>
          </div>
        </section>

        {/* Section 2: StatCards */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">2. StatCards (Standardized Score Labels)</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <StatCard title="Total Interviews" value="12" delta="+2 this week" deltaType="positive" />
            <StatCard title="Average Score" value="78%" delta="+4% this week" deltaType="positive" />
            <StatCard title="Confidence" value="82%" score={82} />
            <StatCard title="Communication" value="75%" score={75} />
            <StatCard title="Grammar" value="88%" score={88} />
            <StatCard title="Resume Score" value="85%" score={85} />
          </div>
        </section>

        {/* Section 3: Score Rings */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">3. Circular Score Donut Rings</h2>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-6 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800">
            <ScoreRing score={92} size={110} subtitle="≥88 Excellent" />
            <ScoreRing score={85} size={110} subtitle="83-87 Very Good" />
            <ScoreRing score={76} size={110} subtitle="70-82 Good" />
            <ScoreRing score={62} size={110} subtitle="55-69 Needs Imprv." />
            <ScoreRing score={45} size={110} subtitle="<55 Needs Practice" />
          </div>
        </section>

        {/* Section 4: Progress, Badges & Toggles */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">4. Progress Bars, Badges, RadioPills & Toggles</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardTitle>Badges & Status</CardTitle>
              <div className="flex flex-wrap gap-2 mt-4">
                <Badge variant="default">Default</Badge>
                <Badge variant="success" dot>Excellent</Badge>
                <Badge variant="info" dot>Very Good</Badge>
                <Badge variant="warning" dot>Good</Badge>
                <Badge variant="danger" dot>Needs Practice</Badge>
                <Badge variant="neutral">Neutral</Badge>
                <Badge variant="outline">Outline</Badge>
              </div>

              <div className="mt-6 space-y-3">
                <ProgressBar value={82} label="Eye Contact Score" showLabel height="h-2" />
                <ProgressBar value={64} label="Voice Clarity" showLabel height="h-2" color="bg-amber-500" />
                <ProgressBar value={92} label="Grammar Accuracy" showLabel height="h-2" color="bg-emerald-500" />
              </div>
            </Card>

            <Card>
              <CardTitle>Controls & Inputs</CardTitle>
              <div className="space-y-5 mt-4">
                <RadioPills
                  options={[
                    { value: 'technical', label: 'Technical' },
                    { value: 'hr', label: 'HR' },
                    { value: 'behavioral', label: 'Behavioral' },
                    { value: 'mixed', label: 'Mixed' },
                  ]}
                  value={radioVal}
                  onChange={setRadioVal}
                />
                <Select
                  label="Target Job Role"
                  options={[
                    { value: 'react', label: 'Frontend Developer (React)' },
                    { value: 'python', label: 'Backend Engineer (FastAPI/Python)' },
                    { value: 'ai', label: 'AI/ML Engineer' },
                  ]}
                  value={selectVal}
                  onChange={setSelectVal}
                />
                <Toggle
                  label="Live AI Analysis"
                  description="Real-time gaze and audio feedback during response"
                  checked={toggleVal}
                  onChange={setToggleVal}
                />
              </div>
            </Card>
          </div>
        </section>

        {/* Section 5: Stepper & Tabs */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">5. Stepper & Tabs</h2>
          <Card>
            <Stepper
              steps={[
                { title: 'Choose Role' },
                { title: 'Question Type' },
                { title: 'Settings' },
                { title: 'Start Interview' },
              ]}
              currentStep={currentStep}
              onStepClick={setCurrentStep}
            />
            <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
              <Tabs
                tabs={[
                  { id: 'buttons', label: 'All Questions', badge: 10 },
                  { id: 'technical', label: 'Technical', badge: 6 },
                  { id: 'hr', label: 'HR & Behavioral', badge: 4 },
                ]}
                activeTab={activeTab}
                onChange={setActiveTab}
              />
            </div>
          </Card>
        </section>

        {/* Section 6: Table */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">6. Data Table & Pagination</h2>
          <Card padding="p-0">
            <div className="p-5 border-b border-slate-100 dark:border-slate-800">
              <h3 className="font-semibold text-sm">Recent Interview Submissions</h3>
            </div>
            <Table
              columns={tableColumns}
              data={tableData}
              currentPage={1}
              totalPages={3}
            />
          </Card>
        </section>

        {/* Section 7: Specialized Widgets */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold">7. Specialized Interview & AI Widgets</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6">
              <WaveformPlayer duration={45} />
              <div className="space-y-3">
                <ChatBubble
                  role="user"
                  content="How can I improve my confidence when answering tricky architectural questions?"
                  userName="Altaf Nadir"
                  timestamp="10:14 AM"
                />
                <ChatBubble
                  role="assistant"
                  content={`1. Pause for 2-3 seconds to structure your thoughts.\n2. State the high-level trade-offs before diving into code.\n3. Keep continuous eye contact with the camera lens.`}
                  timestamp="10:15 AM"
                />
              </div>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <BadgeCard
                  title="First Interview"
                  description="Completed your first AI simulated interview drill."
                  points={50}
                  isUnlocked={true}
                  earnedAt={new Date()}
                />
                <BadgeCard
                  title="Week Streak"
                  description="Practice mock interviews for 7 consecutive days."
                  points={100}
                  isUnlocked={false}
                  progress={{ current: 3, total: 7 }}
                />
              </div>
              <CalendarGrid practicedDays={[2, 3, 4, 10, 11, 12, 18]} />
            </div>
          </div>
        </section>

        {/* Demo Modal */}
        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Component Library Modal"
          description="Demonstrating clean typography, focus trap, and responsive overlay."
          footer={
            <>
              <Button variant="secondary" size="sm" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button variant="primary" size="sm" onClick={() => setIsModalOpen(false)}>
                Confirm Action
              </Button>
            </>
          }
        >
          <p className="text-sm text-slate-600 dark:text-slate-300">
            This modal meets all accessibility requirements, closes on Escape, and integrates seamlessly into light and dark themes.
          </p>
        </Modal>
      </div>
    </div>
  );
}
