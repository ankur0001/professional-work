import type { AIProvider, AnalyzeSpeechInput, ConversationInput, SummaryInput } from "../types";
import { feedbackAnalysisSchema, baselineScoresSchema, sessionSummarySchema } from "@/lib/schemas/feedback";
import { MockAIProvider } from "./mock-ai-provider";

export class OpenAIProvider implements AIProvider {
  name = "openai";
  private fallback = new MockAIProvider();

  private async chatJson(system: string, user: string): Promise<unknown> {
    const key = process.env.OPENAI_API_KEY;
    if (!key) throw new Error("OPENAI_API_KEY missing");
    const model = process.env.OPENAI_MODEL ?? "gpt-4o-mini";
    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        response_format: { type: "json_object" },
        messages: [
          { role: "system", content: system },
          { role: "user", content: user },
        ],
        temperature: 0.4,
      }),
    });
    if (!res.ok) throw new Error(`OpenAI error: ${res.status}`);
    const data = (await res.json()) as { choices: { message: { content: string } }[] };
    const content = data.choices[0]?.message?.content;
    if (!content) throw new Error("Empty OpenAI response");
    return JSON.parse(content);
  }

  async analyzeSpeech(input: AnalyzeSpeechInput) {
    try {
      const { conversationCoachSystem } = await import("@/lib/prompts/conversation-coach");
      const raw = await this.chatJson(
        conversationCoachSystem,
        JSON.stringify({
          task: "analyze_speech",
          ...input,
        }),
      );
      return feedbackAnalysisSchema.parse(raw);
    } catch {
      return this.fallback.analyzeSpeech(input);
    }
  }

  async generateConversationReply(input: ConversationInput) {
    try {
      const key = process.env.OPENAI_API_KEY;
      if (!key) return this.fallback.generateConversationReply(input);
      const model = process.env.OPENAI_MODEL ?? "gpt-4o-mini";
      const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${key}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model,
          messages: input.messages,
          temperature: 0.7,
        }),
      });
      if (!res.ok) throw new Error("OpenAI failed");
      const data = (await res.json()) as { choices: { message: { content: string } }[] };
      return data.choices[0]?.message?.content ?? "";
    } catch {
      return this.fallback.generateConversationReply(input);
    }
  }

  async analyzeBaseline(transcripts: string[]) {
    try {
      const { assessmentCoachSystem } = await import("@/lib/prompts/assessment-coach");
      const raw = await this.chatJson(
        assessmentCoachSystem,
        JSON.stringify({ transcripts }),
      );
      return baselineScoresSchema.parse(raw);
    } catch {
      return this.fallback.analyzeBaseline(transcripts);
    }
  }

  async generateSessionSummary(input: SummaryInput) {
    try {
      const { assessmentCoachSystem } = await import("@/lib/prompts/assessment-coach");
      const raw = await this.chatJson(
        assessmentCoachSystem,
        JSON.stringify({ task: "session_summary", ...input }),
      );
      return sessionSummarySchema.parse(raw);
    } catch {
      return this.fallback.generateSessionSummary(input);
    }
  }

  async coachWriting(input: import("../types").WritingCoachInput) {
    try {
      const { writingCoachSystem } = await import("@/lib/prompts/writing-coach");
      const raw = await this.chatJson(writingCoachSystem, JSON.stringify(input));
      const { writingCoachSchema } = await import("@/lib/schemas/writing");
      return writingCoachSchema.parse(raw);
    } catch {
      return this.fallback.coachWriting(input);
    }
  }

  async evaluateMeetingResponse(input: import("../types").MeetingEvalInput) {
    try {
      const { meetingSimulatorSystem } = await import("@/lib/prompts/meeting-simulator");
      const raw = await this.chatJson(meetingSimulatorSystem, JSON.stringify(input));
      const { meetingEvaluationSchema } = await import("@/lib/schemas/writing");
      return meetingEvaluationSchema.parse(raw);
    } catch {
      return this.fallback.evaluateMeetingResponse(input);
    }
  }

  async analyzeStory(transcript: string) {
    try {
      const { storytellingCoachSystem } = await import("@/lib/prompts/storytelling-coach");
      const raw = await this.chatJson(storytellingCoachSystem, JSON.stringify({ transcript }));
      const { storyAnalysisSchema } = await import("@/lib/schemas/executive");
      return storyAnalysisSchema.parse(raw);
    } catch {
      return this.fallback.analyzeStory(transcript);
    }
  }

  async analyzeExecutivePresentation(input: import("../types").ExecutivePresentationInput) {
    try {
      const { executiveAssessmentSystem } = await import("@/lib/prompts/executive-assessment");
      const raw = await this.chatJson(executiveAssessmentSystem, JSON.stringify(input));
      const { executiveReportSchema } = await import("@/lib/schemas/executive");
      return executiveReportSchema.parse(raw);
    } catch {
      return this.fallback.analyzeExecutivePresentation(input);
    }
  }

  async generateMeetingTurn(input: import("../types").MeetingTurnInput) {
    try {
      const { meetingSimulatorSystem } = await import("@/lib/prompts/meeting-simulator");
      const raw = await this.chatJson(
        meetingSimulatorSystem,
        JSON.stringify({ task: "next_turn", ...input }),
      );
      const { meetingTurnSchema } = await import("@/lib/schemas/executive");
      return meetingTurnSchema.parse(raw);
    } catch {
      return this.fallback.generateMeetingTurn(input);
    }
  }
}
