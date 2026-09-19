import { describe, expect, it } from "vitest";
import { feedbackAnalysisSchema } from "./feedback";

describe("feedbackAnalysisSchema", () => {
  it("validates mock-shaped payload", () => {
    const parsed = feedbackAnalysisSchema.safeParse({
      overallScore: 72,
      fluency: 74,
      grammar: 81,
      vocabulary: 67,
      clarity: 70,
      confidence: 75,
      conciseness: 58,
      leadership: 52,
      mistakes: [],
      betterPhrases: [],
      fillerWords: [],
      coachMessage: "Test",
    });
    expect(parsed.success).toBe(true);
  });

  it("rejects invalid scores", () => {
    const parsed = feedbackAnalysisSchema.safeParse({
      overallScore: 200,
      fluency: 74,
      grammar: 81,
      vocabulary: 67,
      clarity: 70,
      confidence: 75,
      conciseness: 58,
      leadership: 52,
      mistakes: [],
      betterPhrases: [],
      fillerWords: [],
      coachMessage: "Test",
    });
    expect(parsed.success).toBe(false);
  });
});
