import { randomUUID } from "crypto";
import type { BaselineScores } from "@/lib/schemas/feedback";
import { LEVEL_LABELS, levelFromScores } from "@/lib/scoring";

export interface DemoUserProfile {
  id: string;
  email: string;
  name: string;
  profession: string;
  yearsExperience: number;
  englishLevel: string;
  nativeLanguage: string;
  targetAccent: string;
  dailyPracticeMinutes: number;
  primaryGoal: string;
  confidenceScore: number;
  communicationProblems: string[];
  onboardingCompleted: boolean;
  baselineCompleted: boolean;
  currentLevel: number;
  currentLevelLabel: string;
  communicationScores: BaselineScores | Record<string, number>;
  weaknessProfile: Record<string, unknown>;
  streakDays: number;
  totalSpeakingMinutes: number;
  coachPersonality: string;
  sessions: DemoSession[];
  vocabularyItems: VocabularyEntry[];
  achievements: string[];
  completedChallengeIds: string[];
  lastChallengeDate: string | null;
}

export interface VocabularyEntry {
  word: string;
  introducedAt: string;
  dueAt: string;
  useCount: number;
  status: "learning" | "review" | "mastered";
}

export interface DemoSession {
  id: string;
  type: string;
  scenarioTitle: string;
  durationSeconds: number;
  overallScore: number;
  scorecard: Record<string, number>;
  summary: Record<string, unknown>;
  startedAt: string;
}

const DEMO_EMAIL = "demo@executivespeak.app";

let store: DemoUserProfile | null = null;

function defaultProfile(name = "Demo Engineer"): DemoUserProfile {
  const scores: BaselineScores = {
    speakingFluency: 62,
    grammar: 68,
    vocabulary: 55,
    pronunciation: 71,
    clarity: 58,
    confidence: 61,
    leadershipCommunication: 44,
    technicalExplanation: 73,
    conciseness: 49,
    naturalness: 52,
  };
  const level = levelFromScores(scores);
  return {
    id: "demo-user",
    email: DEMO_EMAIL,
    name,
    profession: "Software Engineer",
    yearsExperience: 5,
    englishLevel: "intermediate",
    nativeLanguage: "Hindi",
    targetAccent: "american",
    dailyPracticeMinutes: 20,
    primaryGoal: "leadership",
    confidenceScore: 6,
    communicationProblems: ["fillers", "hesitation"],
    onboardingCompleted: false,
    baselineCompleted: false,
    currentLevel: level,
    currentLevelLabel: LEVEL_LABELS[level] ?? "Professional Communicator",
    communicationScores: scores,
    weaknessProfile: {
      grammarWeaknesses: [],
      fillerWords: ["basically", "maybe"],
      vocabularyWeaknesses: [],
      recurringMistakes: [],
    },
    streakDays: 0,
    totalSpeakingMinutes: 0,
    coachPersonality: "executive_coach",
    sessions: [],
    vocabularyItems: [
      {
        word: "scalable",
        introducedAt: new Date().toISOString(),
        dueAt: new Date().toISOString(),
        useCount: 0,
        status: "learning",
      },
      {
        word: "trade-off",
        introducedAt: new Date().toISOString(),
        dueAt: new Date(Date.now() + 86400000).toISOString(),
        useCount: 0,
        status: "review",
      },
    ],
    achievements: [],
    completedChallengeIds: [],
    lastChallengeDate: null,
  };
}

export function getDemoProfile(email?: string): DemoUserProfile {
  if (!store || (email && store.email !== email)) {
    store = defaultProfile();
  }
  return structuredClone(store);
}

export function saveDemoProfile(profile: DemoUserProfile): DemoUserProfile {
  store = structuredClone(profile);
  return store;
}

export function updateDemoProfile(
  email: string,
  patch: Partial<DemoUserProfile>,
): DemoUserProfile {
  const current = getDemoProfile(email);
  const updated = { ...current, ...patch, email: current.email, id: current.id };
  return saveDemoProfile(updated);
}

const ACHIEVEMENT_RULES: { slug: string; check: (p: DemoUserProfile) => boolean }[] = [
  { slug: "first_conversation", check: (p) => p.sessions.length >= 1 },
  { slug: "ten_minutes", check: (p) => p.totalSpeakingMinutes >= 10 },
  { slug: "hundred_minutes", check: (p) => p.totalSpeakingMinutes >= 100 },
  { slug: "seven_day_streak", check: (p) => p.streakDays >= 7 },
  { slug: "first_leadership_challenge", check: (p) => p.completedChallengeIds.length >= 1 },
];

export function evaluateAchievements(profile: DemoUserProfile): string[] {
  const earned = new Set(profile.achievements);
  for (const rule of ACHIEVEMENT_RULES) {
    if (rule.check(profile)) earned.add(rule.slug);
  }
  return [...earned];
}

export function addDemoSession(email: string, session: Omit<DemoSession, "id">): DemoSession {
  const profile = getDemoProfile(email);
  const full: DemoSession = { ...session, id: randomUUID() };
  profile.sessions.unshift(full);
  profile.totalSpeakingMinutes += Math.round(session.durationSeconds / 60);
  profile.streakDays = Math.max(1, profile.streakDays);
  profile.achievements = evaluateAchievements(profile);
  saveDemoProfile(profile);
  return full;
}

export function completeDailyChallenge(email: string, challengeId: string): DemoUserProfile {
  const profile = getDemoProfile(email);
  const today = new Date().toISOString().slice(0, 10);
  if (!profile.completedChallengeIds.includes(challengeId)) {
    profile.completedChallengeIds.push(challengeId);
  }
  profile.lastChallengeDate = today;
  profile.achievements = evaluateAchievements(profile);
  return saveDemoProfile(profile);
}

export function upsertVocabulary(email: string, words: string[]): DemoUserProfile {
  const profile = getDemoProfile(email);
  for (const word of words) {
    if (profile.vocabularyItems.some((v) => v.word === word)) continue;
    profile.vocabularyItems.push({
      word,
      introducedAt: new Date().toISOString(),
      dueAt: new Date(Date.now() + 3 * 86400000).toISOString(),
      useCount: 0,
      status: "learning",
    });
  }
  return saveDemoProfile(profile);
}

export function reviewVocabularyWord(email: string, word: string, success: boolean): DemoUserProfile {
  const profile = getDemoProfile(email);
  const item = profile.vocabularyItems.find((v) => v.word === word);
  if (!item) return profile;
  if (success) {
    item.useCount += 1;
    item.status = item.useCount >= 3 ? "mastered" : "review";
    item.dueAt = new Date(Date.now() + (success ? 7 : 1) * 86400000).toISOString();
  } else {
    item.dueAt = new Date(Date.now() + 86400000).toISOString();
  }
  if (profile.vocabularyItems.filter((v) => v.status === "mastered").length >= 5) {
    profile.achievements = [...new Set([...profile.achievements, "hundred_new_words"])].slice(0, 20);
  }
  return saveDemoProfile(profile);
}

export function isDemoEmail(email: string): boolean {
  return email === DEMO_EMAIL || email.endsWith("@demo.local");
}

export const DEMO_CREDENTIALS = {
  email: DEMO_EMAIL,
  password: "demo1234",
};
