import type { FeedbackAnalysis, SessionSummary, BaselineScores } from "@/lib/schemas/feedback";

export interface AIProvider {
  name: string;
  analyzeSpeech(input: AnalyzeSpeechInput): Promise<FeedbackAnalysis>;
  generateConversationReply(input: ConversationInput): Promise<string>;
  generateSessionSummary(input: SummaryInput): Promise<SessionSummary>;
  analyzeBaseline(transcripts: string[]): Promise<BaselineScores>;
}

export interface AnalyzeSpeechInput {
  transcript: string;
  scenario: string;
  personality: string;
  previousTranscript?: string;
  mustEvaluateRepeat?: string;
  coachPersonality?: string;
}

export interface ConversationInput {
  messages: { role: "user" | "assistant" | "system"; content: string }[];
  personality: string;
  scenario: string;
}

export interface SummaryInput {
  transcripts: string[];
  analyses: FeedbackAnalysis[];
  scenario: string;
}

export interface SpeechToTextProvider {
  name: string;
  isBrowserSupported(): boolean;
}

export interface TextToSpeechProvider {
  name: string;
  speak(text: string, options?: { rate?: number; accent?: string }): Promise<void>;
}

export interface PronunciationProvider {
  name: string;
  analyzeWord(word: string, transcriptContext: string): Promise<{
    word: string;
    issue: string;
    ipa?: string;
  } | null>;
}
