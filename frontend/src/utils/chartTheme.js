/**
 * Provides theme-aware color tokens for Recharts components
 * across White, Black, Blue, and System themes.
 */

export function getChartTheme(theme, isDark = false) {
  if (theme === 'white' || (!isDark && theme === 'system')) {
    return {
      gridStroke: '#e2e8f0',
      axisStroke: '#64748b',
      axisTickColor: '#64748b',
      tooltipBg: '#ffffff',
      tooltipBorder: '#cbd5e1',
      tooltipTextColor: '#0f172a',
      primaryLine: '#1858e8',
      secondaryLine: '#0bb0e8',
      barColor: '#2563eb',
      radarStroke: '#2563eb',
      radarFill: '#3b82f6',
    };
  }

  if (theme === 'blue') {
    return {
      gridStroke: '#1e3a8a',
      axisStroke: '#93c5fd',
      axisTickColor: '#93c5fd',
      tooltipBg: '#12285c',
      tooltipBorder: '#1e3a8a',
      tooltipTextColor: '#e8f0ff',
      primaryLine: '#60a5fa',
      secondaryLine: '#38bdf8',
      barColor: '#3b82f6',
      radarStroke: '#60a5fa',
      radarFill: '#3b82f6',
    };
  }

  // Black or System (dark)
  return {
    gridStroke: '#27272a',
    axisStroke: '#a1a1aa',
    axisTickColor: '#a1a1aa',
    tooltipBg: '#0a0a0a',
    tooltipBorder: '#27272a',
    tooltipTextColor: '#f8fafc',
    primaryLine: '#6366f1',
    secondaryLine: '#10b981',
    barColor: '#6366f1',
    radarStroke: '#6366f1',
    radarFill: '#818cf8',
  };
}
