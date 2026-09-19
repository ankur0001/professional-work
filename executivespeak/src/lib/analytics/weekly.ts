import type { DemoSession } from "@/lib/demo/demo-store";

export interface WeeklyMetrics {
  weekStart: string;
  speakingMinutes: number;
  sessionCount: number;
  avgOverallScore: number;
  avgClarity: number;
  avgLeadership: number;
  avgFillerEstimate: number;
  vocabularyDiversity: number;
}

export interface WeeklyTrend {
  current: WeeklyMetrics;
  previous: WeeklyMetrics | null;
  deltas: Record<string, number | null>;
}

function weekStart(date: Date): Date {
  const d = new Date(date);
  const day = d.getUTCDay();
  const diff = (day + 6) % 7;
  d.setUTCDate(d.getUTCDate() - diff);
  d.setUTCHours(0, 0, 0, 0);
  return d;
}

function sessionsInWeek(sessions: DemoSession[], start: Date): DemoSession[] {
  const end = new Date(start);
  end.setUTCDate(end.getUTCDate() + 7);
  return sessions.filter((s) => {
    const t = new Date(s.startedAt);
    return t >= start && t < end;
  });
}

function computeMetrics(sessions: DemoSession[], start: Date): WeeklyMetrics {
  const weekSessions = sessionsInWeek(sessions, start);
  const speakingMinutes = weekSessions.reduce((m, s) => m + Math.round(s.durationSeconds / 60), 0);
  const avg = (key: string) => {
    const vals = weekSessions.map((s) => s.scorecard[key]).filter((v) => typeof v === "number") as number[];
    return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
  };
  const avgOverall =
    weekSessions.length > 0
      ? Math.round(weekSessions.reduce((a, s) => a + s.overallScore, 0) / weekSessions.length)
      : 0;

  return {
    weekStart: start.toISOString().slice(0, 10),
    speakingMinutes,
    sessionCount: weekSessions.length,
    avgOverallScore: avgOverall,
    avgClarity: avg("clarity"),
    avgLeadership: avg("leadership"),
    avgFillerEstimate: 0,
    vocabularyDiversity: avg("vocabulary"),
  };
}

export function computeWeeklyTrend(sessions: DemoSession[], now = new Date()): WeeklyTrend {
  const currentStart = weekStart(now);
  const previousStart = new Date(currentStart);
  previousStart.setUTCDate(previousStart.getUTCDate() - 7);

  const current = computeMetrics(sessions, currentStart);
  const previous = computeMetrics(sessions, previousStart);

  const deltas: Record<string, number | null> = {};
  if (previous.sessionCount > 0 && current.sessionCount > 0) {
    deltas.avgOverallScore = current.avgOverallScore - previous.avgOverallScore;
    deltas.avgClarity = current.avgClarity - previous.avgClarity;
    deltas.avgLeadership = current.avgLeadership - previous.avgLeadership;
    deltas.vocabularyDiversity = current.vocabularyDiversity - previous.vocabularyDiversity;
    deltas.speakingMinutes = current.speakingMinutes - previous.speakingMinutes;
  } else {
    deltas.avgOverallScore = null;
  }

  return {
    current,
    previous: previous.sessionCount > 0 ? previous : null,
    deltas,
  };
}
