import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { getScoreRating } from '../utils/scoreRating';
import ScoreRing from '../components/ui/ScoreRing';
import StatCard from '../components/ui/StatCard';
import Button from '../components/ui/Button';

describe('Design System - Standardized Score Rating System', () => {
  it('correctly classifies score >= 88 as Excellent', () => {
    const res = getScoreRating(92);
    expect(res.label).toBe('Excellent');
    expect(res.variant).toBe('success');
    expect(res.color).toBe('#10B981');
  });

  it('correctly classifies score 83-87 as Very Good', () => {
    const res = getScoreRating(85);
    expect(res.label).toBe('Very Good');
    expect(res.variant).toBe('info');
    expect(res.color).toBe('#0EA5E9');
  });

  it('correctly classifies score 70-82 as Good', () => {
    const res = getScoreRating(78);
    expect(res.label).toBe('Good');
    expect(res.variant).toBe('warning');
    expect(res.color).toBe('#F59E0B');
  });

  it('correctly classifies score 55-69 as Needs Improvement', () => {
    const res = getScoreRating(64);
    expect(res.label).toBe('Needs Improvement');
    expect(res.variant).toBe('orange');
    expect(res.color).toBe('#F97316');
  });

  it('correctly classifies score < 55 as Needs Practice', () => {
    const res = getScoreRating(42);
    expect(res.label).toBe('Needs Practice');
    expect(res.variant).toBe('danger');
    expect(res.color).toBe('#EF4444');
  });

  it('handles null/undefined gracefully', () => {
    const res = getScoreRating(null);
    expect(res.label).toBe('Not analyzed yet');
  });
});

describe('Design System - UI Components', () => {
  it('renders ScoreRing with percentage and rating', () => {
    render(<ScoreRing score={89} />);
    expect(screen.getByText('89%')).toBeInTheDocument();
    expect(screen.getByText('Excellent')).toBeInTheDocument();
  });

  it('renders StatCard with value and delta', () => {
    render(
      <StatCard
        title="Total Interviews"
        value="12"
        delta="+2 this week"
        deltaType="positive"
      />
    );
    expect(screen.getByText('Total Interviews')).toBeInTheDocument();
    expect(screen.getByText('12')).toBeInTheDocument();
    expect(screen.getByText(/2 this week/)).toBeInTheDocument();
  });

  it('renders Button with variants and loading state', () => {
    const { rerender } = render(<Button variant="primary">Start Free</Button>);
    expect(screen.getByRole('button', { name: /Start Free/i })).toBeInTheDocument();

    rerender(<Button variant="primary" loading>Start Free</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
