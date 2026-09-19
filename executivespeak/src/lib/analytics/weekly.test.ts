import { describe, expect, it } from "vitest";
import { computeWeeklyTrend } from "./weekly";
import type { DemoSession } from "@/lib/demo/demo-store";

describe("computeWeeklyTrend", () => {
  it("returns null deltas when insufficient history", () => {
    const trend = computeWeeklyTrend([]);
    expect(trend.current.sessionCount).toBe(0);
    expect(trend.deltas.avgOverallScore).toBeNull();
  });

  it("computes averages for sessions in current week", () => {
    const now = new Date();
    const sessions: DemoSession[] = [
      {
        id: "1",
        type: "practice",
        scenarioTitle: "Test",
        durationSeconds: 600,
        overallScore: 70,
        scorecard: { clarity: 65, leadership: 55 },
        summary: {},
        startedAt: now.toISOString(),
      },
    ];
    const trend = computeWeeklyTrend(sessions, now);
    expect(trend.current.sessionCount).toBe(1);
    expect(trend.current.avgOverallScore).toBe(70);
  });
});
