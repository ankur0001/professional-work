import { describe, expect, it } from "vitest";
import { buildPersonalizedPlan } from "./personalize";

describe("buildPersonalizedPlan", () => {
  it("targets leadership when leadership score is low", () => {
    const plan = buildPersonalizedPlan({
      communicationProblems: ["fillers", "confidence"],
      communicationScores: { leadershipCommunication: 44, conciseness: 49 },
      dailyPracticeMinutes: 20,
    });
    expect(plan.weaknessTargets.length).toBeGreaterThan(0);
    expect(plan.items.length).toBeGreaterThan(0);
  });
});
