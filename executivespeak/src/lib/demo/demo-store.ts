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

export function addDemoSession(email: string, session: Omit<DemoSession, "id">): DemoSession {
  const profile = getDemoProfile(email);
  const full: DemoSession = { ...session, id: randomUUID() };
  profile.sessions.unshift(full);
  profile.totalSpeakingMinutes += Math.round(session.durationSeconds / 60);
  profile.streakDays = Math.max(1, profile.streakDays);
  saveDemoProfile(profile);
  return full;
}

export function isDemoEmail(email: string): boolean {
  return email === DEMO_EMAIL || email.endsWith("@demo.local");
}

export const DEMO_CREDENTIALS = {
  email: DEMO_EMAIL,
  password: "demo1234",
};
