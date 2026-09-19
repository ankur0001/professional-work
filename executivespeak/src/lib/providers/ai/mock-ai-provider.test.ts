import { describe, expect, it } from "vitest";
import { MockAIProvider } from "./mock-ai-provider";

describe("MockAIProvider", () => {
  const ai = new MockAIProvider();

  it("returns validated analysis", async () => {
    const result = await ai.analyzeSpeech({
      transcript: "I think basically maybe we can try to change this architecture.",
      scenario: "Migration",
      personality: "executive_coach",
    });
    expect(result.overallScore).toBeGreaterThan(0);
    expect(result.mustRepeatPhrase).toBeTruthy();
  });

  it("handles missing API gracefully via mock baseline", async () => {
    const scores = await ai.analyzeBaseline(["I work on backend services."]);
    expect(scores.speakingFluency).toBeGreaterThan(0);
  });
});
