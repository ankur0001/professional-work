import { describe, expect, it } from "vitest";
import { averageScore, detectFillerWords, levelFromScores, computeOverallFromFeedback } from "./scoring";
import type { FeedbackAnalysis } from "./schemas/feedback";

describe("scoring", () => {
  it("averages scores", () => {
    expect(averageScore([60, 80])).toBe(70);
  });

  it("detects filler words", () => {
    const r = detectFillerWords("Basically, I think maybe we should, um, like, you know, proceed.");
    expect(r.some((x) => x.word === "basically")).toBe(true);
    expect(r.some((x) => x.word === "I think")).toBe(true);
  });

  it("maps level from baseline scores", () => {
    expect(levelFromScores({ a: 40, b: 40 })).toBe(1);
    expect(levelFromScores({ a: 88, b: 88 })).toBeGreaterThanOrEqual(6);
  });

  it("computes overall feedback score", () => {
    const f = {
      fluency: 70,
      grammar: 80,
      vocabulary: 60,
      clarity: 75,
      confidence: 72,
      conciseness: 65,
      leadership: 55,
      pronunciation: 78,
    } as FeedbackAnalysis;
    expect(computeOverallFromFeedback(f)).toBeGreaterThan(60);
  });
});
