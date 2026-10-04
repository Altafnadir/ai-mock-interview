import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import LandingPage from '../pages/public/LandingPage';
import LoginPage from '../pages/auth/LoginPage';
import DashboardPage from '../pages/candidate/DashboardPage';
import ResumePage from '../pages/candidate/ResumePage';
import { dashboardApi } from '../api/dashboard';
import { resumeApi } from '../api/resume';

vi.mock('../api/dashboard', () => ({
  dashboardApi: {
    getOverview: vi.fn(),
    getPerformance: vi.fn(),
    getRecommendation: vi.fn(),
    getTrends: vi.fn(),
    compareSessions: vi.fn(),
  },
}));

vi.mock('../api/resume', () => ({
  resumeApi: {
    getResumes: vi.fn(),
    getResumeAnalysis: vi.fn(),
    uploadResume: vi.fn(),
    reanalyzeResume: vi.fn(),
    getFullAnalysis: vi.fn(),
    deleteResume: vi.fn(),
  },
}));

describe('Phase 1 Pages: Exact-Match Screens', () => {
  it('Screen 1: LandingPage renders exact hero headline, sample report card, and demo modal trigger', async () => {
    render(
      <BrowserRouter>
        <LandingPage />
      </BrowserRouter>
    );

    // Headline check
    expect(screen.getByText(/ace every interview with/i)).toBeInTheDocument();
    expect(screen.getByText(/ai confidence/i)).toBeInTheDocument();
    expect(screen.getAllByText(/start free interview/i).length).toBeGreaterThan(0);

    // Sample report card on right
    expect(screen.getByText(/sample report/i)).toBeInTheDocument();
    expect(screen.getByText(/89%/i)).toBeInTheDocument();
    expect(screen.getByText(/performance trend/i)).toBeInTheDocument();
    expect(screen.getByText(/\+15% this week/i)).toBeInTheDocument();

    // Truthful FYP attribution
    expect(screen.getAllByText(/final-year project/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/pmas-arid agriculture university/i).length).toBeGreaterThan(0);

    // Watch Demo Modal
    const demoBtn = screen.getByRole('button', { name: /watch demo/i });
    fireEvent.click(demoBtn);
    expect(screen.getByText(/interactive platform walkthrough/i)).toBeInTheDocument();
  });

  it('Screen 2: LoginPage renders auth split layout with dark navy panel and form', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    // Left hero panel
    expect(screen.getByText(/sign in to continue your interview preparation journey/i)).toBeInTheDocument();

    // Right form card
    expect(screen.getByPlaceholderText(/student@gims\.edu\.pk/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/••••••••/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^sign in$/i })).toBeInTheDocument();
    expect(screen.getByText(/continue with/i)).toBeInTheDocument();
    expect(screen.getByText(/google/i)).toBeInTheDocument();
  });

  it('Screen 3: DashboardPage renders 6 stat cards, Performance Overview, and AI Recommendation', async () => {
    dashboardApi.getOverview.mockResolvedValueOnce({
      data: {
        metrics: {
          total_interviews: 12,
          average_score: 78.0,
          confidence_score: 82.0,
          communication_score: 75.0,
          grammar_score: 88.0,
          resume_score: 85.0,
          practice_streak_days: 7,
          interviews_delta_week: 2,
          score_delta_week: 4.0,
          next_goal: { text: 'Complete 3 interviews this week', current: 1, target: 3 },
        },
        recent_sessions: [
          {
            id: 'sess-1',
            role_name: 'Frontend Developer',
            category_name: 'Technical',
            score: 90.0,
            date: 'May 12, 2024',
          },
        ],
        ai_recommendation: {
          text: 'Focus on improving your eye contact and reducing filler words.',
          action_text: 'Start Recommended Practice',
        },
      },
    });

    dashboardApi.getPerformance.mockResolvedValueOnce({
      data: {
        range: 'week',
        data: [
          { label: 'Mon', score: 65 },
          { label: 'Tue', score: 72 },
          { label: 'Wed', score: 78 },
        ],
      },
    });

    render(
      <BrowserRouter>
        <DashboardPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      // 6 Stat cards
      expect(screen.getByText('Total Interviews')).toBeInTheDocument();
      expect(screen.getByText('Average Score')).toBeInTheDocument();
      expect(screen.getByText('Confidence')).toBeInTheDocument();
      expect(screen.getByText('Communication')).toBeInTheDocument();
      expect(screen.getByText('Grammar')).toBeInTheDocument();
      expect(screen.getByText('Resume Score')).toBeInTheDocument();

      // Performance Overview
      expect(screen.getByText(/performance overview/i)).toBeInTheDocument();
      expect(screen.getByRole('combobox', { name: /performance time range/i })).toBeInTheDocument();

      // AI Recommendation
      expect(screen.getByText(/ai recommendation/i)).toBeInTheDocument();
      expect(screen.getByText(/focus on improving your eye contact/i)).toBeInTheDocument();

      // Streak & Next goal
      expect(screen.getByText('7 Days')).toBeInTheDocument();
      expect(screen.getByText(/practice streak/i)).toBeInTheDocument();
      expect(screen.getByText(/next goal/i)).toBeInTheDocument();
    });
  });

  it('Screen 4: ResumePage renders score ring, top skills list, 3 info cards, and strengths/improvements', async () => {
    resumeApi.getResumes.mockResolvedValueOnce({
      data: [
        {
          id: 'res-v2',
          original_filename: 'Hussnain_Resume.pdf',
          file_type: 'pdf',
          uploaded_at: '2024-05-10T10:00:00Z',
          is_active: true,
        },
      ],
    });

    resumeApi.getResumeAnalysis.mockResolvedValueOnce({
      data: {
        resume_score: 87.0,
        score_label: 'Very Good',
        top_skills: ['React.js', 'JavaScript', 'Python', 'Node.js', 'SQL', 'Git', 'Docker'],
        years_experience: 2.0,
        projects_count: 5,
        strengths: ['Strong technical knowledge', 'Clean full-stack portfolio'],
        areas_to_improve: ['Include quantifiable metrics', 'Add cloud certifications'],
      },
    });

    render(
      <BrowserRouter>
        <ResumePage />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Header card
      expect(screen.getByText(/hussnain_resume\.pdf/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /re-analyze/i })).toBeInTheDocument();

      // Score Ring
      expect(screen.getAllByText(/87%/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/very good/i).length).toBeGreaterThan(0);

      // Top Skills
      expect(screen.getByText(/top skills found/i)).toBeInTheDocument();
      expect(screen.getByText('React.js')).toBeInTheDocument();
      expect(screen.getByText('JavaScript')).toBeInTheDocument();
      expect(screen.getByText(/\+ 1 more/i)).toBeInTheDocument();

      // 3 Info Cards
      expect(screen.getByText('2+ Years')).toBeInTheDocument();
      expect(screen.getByText('5 Projects')).toBeInTheDocument();

      // Strengths & Improvements
      expect(screen.getByText(/strong technical knowledge/i)).toBeInTheDocument();
      expect(screen.getByText(/include quantifiable metrics/i)).toBeInTheDocument();

      // View Full Analysis Button
      expect(screen.getByRole('button', { name: /view full analysis/i })).toBeInTheDocument();
    });
  });
});
