import { z } from "zod";

export const storyAnalysisSchema = z.object({
  situation: z.number().min(0).max(100),
  challenge: z.number().min(0).max(100),
  action: z.number().min(0).max(100),
  result: z.number().min(0).max(100),
  lesson: z.number().min(0).max(100),
  overall: z.number().min(0).max(100),
  structureNotes: z.string(),
  improvedOutline: z.string(),
});

export type StoryAnalysis = z.infer<typeof storyAnalysisSchema>;

export const executiveReportSchema = z.object({
  executivePresence: z.number().min(0).max(100),
  clarity: z.number().min(0).max(100),
  conciseness: z.number().min(0).max(100),
  structure: z.number().min(0).max(100),
  businessAwareness: z.number().min(0).max(100),
  technicalDepth: z.number().min(0).max(100),
  confidence: z.number().min(0).max(100),
  persuasiveness: z.number().min(0).max(100),
  audienceAdaptation: z.number().min(0).max(100),
  overall: z.number().min(0).max(100),
  coachingReport: z.string(),
  topThreeActions: z.array(z.string()).length(3),
});

export type ExecutiveReport = z.infer<typeof executiveReportSchema>;

export const meetingTurnSchema = z.object({
  speaker: z.string(),
  line: z.string(),
  expectsUserResponse: z.boolean(),
});

export type MeetingTurn = z.infer<typeof meetingTurnSchema>;
