import { SCENARIOS, type ScenarioDefinition } from "@/lib/data/scenarios";

export interface WeaknessProfile {
  grammarWeaknesses?: string[];
  fillerWords?: string[];
  vocabularyWeaknesses?: string[];
  communicationWeaknesses?: string[];
  leadershipWeaknesses?: string[];
}

export interface PersonalizedPlan {
  focus: string;
  minutes: number;
  weaknessTargets: string[];
  items: ScenarioDefinition[];
}

const CATEGORY_BY_WEAKNESS: Record<string, ScenarioDefinition["category"][]> = {
  fillers: ["presentation", "impromptu"],
  hesitation: ["impromptu", "warmup"],
  grammar: ["technical", "warmup"],
  vocabulary: ["technical", "presentation"],
  pronunciation: ["warmup", "presentation"],
  clarity: ["presentation", "leadership"],
  confidence: ["leadership", "impromptu"],
  leadership: ["leadership", "meeting"],
};

export function buildPersonalizedPlan(
  profile: {
    dailyPracticeMinutes?: number;
    communicationScores?: Record<string, number>;
    weaknessProfile?: WeaknessProfile;
    communicationProblems?: string[];
  },
): PersonalizedPlan {
  const scores = profile.communicationScores ?? {};
  const weakDimensions = Object.entries(scores)
    .filter(([, v]) => typeof v === "number" && v < 60)
    .map(([k]) => k);

  const problems = profile.communicationProblems ?? [];
  const fillerWords = profile.weaknessProfile?.fillerWords ?? [];
  const targets: string[] = [];
  if (fillerWords.length) targets.push("Reduce fillers — pause instead of hedging");
  if (weakDimensions.includes("leadershipCommunication") || problems.includes("confidence")) {
    targets.push("Speak with clearer recommendations");
  }
  if (weakDimensions.includes("conciseness")) targets.push("Shorter executive updates");

  const categories = new Set<ScenarioDefinition["category"]>();
  for (const p of problems) {
    for (const c of CATEGORY_BY_WEAKNESS[p] ?? []) categories.add(c);
  }
  if (categories.size === 0) {
    categories.add("leadership");
    categories.add("technical");
  }

  const items = SCENARIOS.filter((s) => categories.has(s.category)).slice(0, 5);
  const fallback = SCENARIOS.slice(0, 5);
  const chosen = items.length >= 3 ? items : fallback;

  return {
    focus: targets[0] ?? "Speaking with more clarity and authority",
    minutes: profile.dailyPracticeMinutes ?? 20,
    weaknessTargets: targets.length ? targets : ["Executive clarity in recommendations"],
    items: chosen,
  };
}
