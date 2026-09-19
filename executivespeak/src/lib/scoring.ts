import type { FeedbackAnalysis } from "@/lib/schemas/feedback";
import type { BaselineScores } from "@/lib/schemas/feedback";

export const LEVEL_LABELS: Record<number, string> = {
  1: "Basic Speaker",
  2: "Functional Speaker",
  3: "Confident Speaker",
  4: "Professional Communicator",
  5: "Senior Communicator",
  6: "Leadership Communicator",
  7: "Executive Communicator",
};

export function averageScore(scores: number[]): number {
  if (scores.length === 0) return 0;
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
}

export function computeOverallFromFeedback(f: FeedbackAnalysis): number {
  return averageScore([
    f.fluency,
    f.grammar,
    f.vocabulary,
    f.clarity,
    f.confidence,
    f.conciseness,
    f.leadership,
    f.pronunciation ?? f.clarity,
  ]);
}

export function detectFillerWords(transcript: string): { word: string; count: number }[] {
  const fillers = [
    "um",
    "uh",
    "like",
    "basically",
    "actually",
    "you know",
    "so",
    "maybe",
    "kind of",
    "sort of",
  ];
  const lower = transcript.toLowerCase();
  const results: { word: string; count: number }[] = [];
  for (const f of fillers) {
    const regex = new RegExp(`\\b${f.replace(/ /g, "\\s+")}\\b`, "gi");
    const matches = lower.match(regex);
    if (matches?.length) results.push({ word: f, count: matches.length });
  }
  const thinkMatches = lower.match(/\bi think\b/gi);
  if (thinkMatches?.length) {
    results.push({ word: "I think", count: thinkMatches.length });
  }
  return results.sort((a, b) => b.count - a.count);
}

export function levelFromScores(scores: BaselineScores | Record<string, number>): number {
  const values = Object.values(scores);
  const avg = averageScore(values);
  if (avg >= 85) return 7;
  if (avg >= 78) return 6;
  if (avg >= 70) return 5;
  if (avg >= 62) return 4;
  if (avg >= 54) return 3;
  if (avg >= 45) return 2;
  return 1;
}

export function mergeWeaknessProfile(
  existing: Record<string, unknown> | null | undefined,
  analysis: FeedbackAnalysis,
): Record<string, unknown> {
  const profile = (existing ?? {}) as {
    grammarWeaknesses?: string[];
    fillerWords?: string[];
    vocabularyWeaknesses?: string[];
    recurringMistakes?: string[];
  };
  const grammarWeaknesses = new Set(profile.grammarWeaknesses ?? []);
  for (const m of analysis.mistakes) {
    grammarWeaknesses.add(`${m.original} → ${m.correction}`);
  }
  const fillerWords = new Set(profile.fillerWords ?? []);
  for (const f of analysis.fillerWords) {
    if (f.count >= 2) fillerWords.add(f.word);
  }
  return {
    ...profile,
    grammarWeaknesses: [...grammarWeaknesses].slice(-20),
    fillerWords: [...fillerWords].slice(-15),
    lastUpdated: new Date().toISOString(),
  };
}
