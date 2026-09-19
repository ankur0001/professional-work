import type {
  AIProvider,
  AnalyzeSpeechInput,
  ConversationInput,
  SummaryInput,
  WritingCoachInput,
  MeetingEvalInput,
} from "../types";
import { feedbackAnalysisSchema } from "@/lib/schemas/feedback";
import { writingCoachSchema, meetingEvaluationSchema } from "@/lib/schemas/writing";
import { detectFillerWords } from "@/lib/scoring";

function scoreFromText(transcript: string, base: number): number {
  const words = transcript.split(/\s+/).filter(Boolean).length;
  const fillers = detectFillerWords(transcript);
  const fillerPenalty = Math.min(15, fillers.reduce((s, f) => s + f.count, 0) * 2);
  const lengthBonus = Math.min(10, Math.floor(words / 20));
  return Math.max(40, Math.min(92, base - fillerPenalty + lengthBonus));
}

export class MockAIProvider implements AIProvider {
  name = "mock";

  async analyzeSpeech(input: AnalyzeSpeechInput) {
    const t = input.transcript.trim();
    const fillers = detectFillerWords(t);
    const fillerTotal = fillers.reduce((s, f) => s + f.count, 0);

    const weakPattern =
      /\b(basically|maybe|kind of|sort of|I think maybe)\b/i.test(t) ||
      /\bcurrently it is having\b/i.test(t);

    const natural =
      "I think we should consider changing the architecture because the current design has several issues.";
    const professional =
      "I have some concerns about this approach, particularly around scalability and maintainability.";
    const leadership =
      "I recommend we revisit the architecture because the current design is creating several problems. Let's evaluate two alternatives before we commit.";

    let coachMessage =
      "Your message was understandable. Let's sharpen clarity and reduce indirect language.";
    let mustRepeatPhrase: string | undefined = leadership;

    if (input.mustEvaluateRepeat) {
      const target = input.mustEvaluateRepeat.toLowerCase();
      const said = t.toLowerCase();
      const overlap = target.split(" ").filter((w) => w.length > 4 && said.includes(w)).length;
      if (overlap >= 4) {
        coachMessage =
          "Much stronger. Your recommendation landed clearly. I'll push back as your manager — respond with the same direct tone.";
        mustRepeatPhrase = undefined;
      } else {
        coachMessage =
          "Good effort. Try again with a clearer recommendation — start with 'I recommend' and state the business reason in one sentence.";
        mustRepeatPhrase = input.mustEvaluateRepeat;
      }
    } else if (weakPattern || fillerTotal >= 4) {
      coachMessage =
        "You were understandable, but too indirect. You used hedging and fillers that weaken executive presence. Try the leadership version in your own words.";
    } else if (t.length < 40) {
      coachMessage = "Expand slightly — add one concrete reason or example so your point lands with stakeholders.";
    } else {
      coachMessage =
        "Solid explanation. Next I'll challenge your proposal — stay concise and confident.";
      mustRepeatPhrase = undefined;
    }

    const raw = {
      overallScore: scoreFromText(t, 72),
      fluency: scoreFromText(t, 74),
      grammar: scoreFromText(t, 78),
      vocabulary: scoreFromText(t, 68),
      pronunciation: 75,
      clarity: scoreFromText(t, 70),
      confidence: scoreFromText(t, 72),
      conciseness: Math.max(45, 72 - fillerTotal * 3),
      leadership: weakPattern ? 52 : scoreFromText(t, 65),
      technicalCommunication: scoreFromText(t, 76),
      mistakes: weakPattern
        ? [
            {
              original: "maybe we can try",
              correction: "we should",
              explanation: "Replace tentative phrasing with a clear recommendation.",
              category: "hedging",
            },
          ]
        : [],
      betterPhrases: [
        {
          natural,
          professional,
          leadership,
          notes: "Removed fillers, strengthened the recommendation, improved executive clarity.",
        },
      ],
      fillerWords: fillers.map((f) => ({
        word: f.word,
        count: f.count,
        suggestion:
          f.word === "basically" || f.word === "maybe"
            ? "Lead with: 'I recommend…'"
            : undefined,
      })),
      pronunciationIssues: /\barchitec/i.test(t)
        ? [{ word: "architecture", issue: "Stress on second syllable: ar-KI-tec-ture", ipa: "/ˈɑːrkɪtektʃər/" }]
        : [],
      coachMessage,
      mustRepeatPhrase,
      nextPrompt:
        mustRepeatPhrase === undefined
          ? "I'm concerned about the migration timeline. Why should we prioritize this quarter?"
          : undefined,
    };

    return feedbackAnalysisSchema.parse(raw);
  }

  async generateConversationReply(input: ConversationInput): Promise<string> {
    const lastUser = [...input.messages].reverse().find((m) => m.role === "user");
    if (!lastUser) {
      return `You're presenting a proposal to your manager. Explain why you want to migrate the service to a new architecture.`;
    }
    return `Thanks — I hear your point. What risks should we watch during migration, and what's the smallest first step?`;
  }

  async analyzeBaseline(transcripts: string[]): Promise<import("@/lib/schemas/feedback").BaselineScores> {
    const combined = transcripts.join(" ");
    const base = scoreFromText(combined, 62);
    return {
      speakingFluency: base,
      grammar: base + 6,
      vocabulary: base - 7,
      pronunciation: base + 9,
      clarity: base - 4,
      confidence: base + 1,
      leadershipCommunication: base - 18,
      technicalExplanation: base + 11,
      conciseness: base - 13,
      naturalness: base - 10,
    };
  }

  async generateSessionSummary(input: SummaryInput) {
    const fillers = input.analyses.flatMap((a) => a.fillerWords);
    const totalFillers = fillers.reduce((s, f) => s + f.count, 0);
    return {
      strengths: [
        "You stayed on topic and answered the scenario directly.",
        "Your technical intent came through even when phrasing was indirect.",
        "You completed the repeat exercise, which builds muscle memory for stronger phrases.",
      ],
      improvements: [
        totalFillers > 5
          ? "Reduce filler words — pause briefly instead of saying 'um' or 'basically'."
          : "Tighten openings — lead with your recommendation in the first sentence.",
        "Use stronger verbs: recommend, propose, prioritize instead of 'maybe' and 'try'.",
        "Close with a clear next step or ask to sound leadership-ready.",
      ],
      topMistake: "Hedging with 'I think maybe' instead of stating a recommendation.",
      betterPhrase: "I recommend we revisit the architecture because the current design is creating several problems.",
      tomorrowChallenge: "Give a 60-second project update to a non-technical manager — no fillers in the first sentence.",
    };
  }

  async coachWriting(input: WritingCoachInput) {
    const t = input.text.trim();
    const hedging = /\b(maybe|just|sorry|I think)\b/i.test(t);
    return writingCoachSchema.parse({
      original: t,
      corrected: t.replace(/\bmaybe\b/gi, "").replace(/\s+/g, " ").trim(),
      natural: hedging
        ? "Thanks for the update. I have concerns about the Friday date — here's what we can ship safely."
        : t,
      professional:
        "Thanks for raising this. A Friday release is risky given open integration work. I recommend we ship a scoped MVP Friday and schedule the remainder for the next sprint.",
      leadership:
        "A Friday launch would expose us to integration risk. My recommendation: deliver the core workflow Friday with feature flags, and commit the remaining scope by next Wednesday.",
      toneNotes: hedging
        ? "You sound apologetic. Lead with your recommendation, not uncertainty."
        : "Tone is neutral; strengthen with a clear recommendation.",
      clarityNotes: "State the risk, the proposal, and the next step in three sentences.",
      shorter:
        "Friday is too aggressive for full scope. Recommend MVP Friday + remainder next sprint.",
      moreConfident: "We should not commit to the full feature by Friday. We will deliver the MVP and defer non-critical scope.",
      moreDiplomatic:
        "I hear the urgency. To protect quality, I'd suggest we align on a reduced scope for Friday and plan the rest immediately after.",
      executiveFriendly:
        "Risk: full feature by Friday. Proposal: MVP Friday, complete rollout next week. Decision needed: approve reduced scope?",
    });
  }

  async evaluateMeetingResponse(input: MeetingEvalInput) {
    const t = input.userResponse.trim();
    const base = scoreFromText(t, 68);
    const weak = /\b(maybe|sorry|I guess)\b/i.test(t);
    return meetingEvaluationSchema.parse({
      clear: base,
      professional: weak ? base - 8 : base + 4,
      assertive: weak ? base - 12 : base,
      collaborative: base + 2,
      leadership: weak ? base - 10 : base + 6,
      summary: weak
        ? "You addressed the question, but hedging weakened your authority. Name the trade-off and propose a concrete plan."
        : "Solid meeting response — you balanced constraints with a clear recommendation.",
      improvedVersion:
        "I understand the Friday deadline. Adding people won't help this week due to onboarding cost. I recommend we ship auth + checkout Friday and move reporting to sprint 24 — I'll document scope for PM sign-off today.",
    });
  }
}
