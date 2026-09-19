import { z } from "zod";

export const writingCoachSchema = z.object({
  original: z.string(),
  corrected: z.string(),
  natural: z.string(),
  professional: z.string(),
  leadership: z.string(),
  toneNotes: z.string(),
  clarityNotes: z.string(),
  shorter: z.string().optional(),
  moreConfident: z.string().optional(),
  moreDiplomatic: z.string().optional(),
  executiveFriendly: z.string().optional(),
});

export type WritingCoachResult = z.infer<typeof writingCoachSchema>;

export const meetingEvaluationSchema = z.object({
  clear: z.number().min(0).max(100),
  professional: z.number().min(0).max(100),
  assertive: z.number().min(0).max(100),
  collaborative: z.number().min(0).max(100),
  leadership: z.number().min(0).max(100),
  summary: z.string(),
  improvedVersion: z.string(),
});

export type MeetingEvaluation = z.infer<typeof meetingEvaluationSchema>;
