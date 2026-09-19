import { z } from "zod";

export const feedbackAnalysisSchema = z.object({
  overallScore: z.number().min(0).max(100),
  fluency: z.number().min(0).max(100),
  grammar: z.number().min(0).max(100),
  vocabulary: z.number().min(0).max(100),
  pronunciation: z.number().min(0).max(100).optional(),
  clarity: z.number().min(0).max(100),
  confidence: z.number().min(0).max(100),
  conciseness: z.number().min(0).max(100),
  leadership: z.number().min(0).max(100),
  technicalCommunication: z.number().min(0).max(100).optional(),
  storytelling: z.number().min(0).max(100).optional(),
  mistakes: z.array(
    z.object({
      original: z.string(),
      correction: z.string(),
      explanation: z.string().optional(),
      category: z.string().optional(),
    }),
  ),
  betterPhrases: z.array(
    z.object({
      natural: z.string(),
      professional: z.string(),
      leadership: z.string(),
      notes: z.string().optional(),
    }),
  ),
  fillerWords: z.array(
    z.object({
      word: z.string(),
      count: z.number(),
      suggestion: z.string().optional(),
    }),
  ),
  pronunciationIssues: z
    .array(
      z.object({
        word: z.string(),
        issue: z.string(),
        ipa: z.string().optional(),
      }),
    )
    .optional(),
  coachMessage: z.string(),
  mustRepeatPhrase: z.string().optional(),
  nextPrompt: z.string().optional(),
  nextExercise: z.string().optional(),
});

export type FeedbackAnalysis = z.infer<typeof feedbackAnalysisSchema>;

export const sessionSummarySchema = z.object({
  strengths: z.array(z.string()).length(3),
  improvements: z.array(z.string()).length(3),
  topMistake: z.string(),
  betterPhrase: z.string(),
  tomorrowChallenge: z.string(),
});

export type SessionSummary = z.infer<typeof sessionSummarySchema>;

export const baselineScoresSchema = z.object({
  speakingFluency: z.number(),
  grammar: z.number(),
  vocabulary: z.number(),
  pronunciation: z.number(),
  clarity: z.number(),
  confidence: z.number(),
  leadershipCommunication: z.number(),
  technicalExplanation: z.number(),
  conciseness: z.number(),
  naturalness: z.number(),
});

export type BaselineScores = z.infer<typeof baselineScoresSchema>;
