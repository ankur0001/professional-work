import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import {
  addDemoSession,
  completeDailyChallenge,
  getDemoProfile,
  saveDemoProfile,
  upsertVocabulary,
} from "@/lib/demo/demo-store";
import { getDailyChallenge } from "@/lib/data/daily-challenges";
import { suggestWordsFromTranscript } from "@/lib/vocabulary/suggest";
import { detectWordsInTranscript } from "@/lib/providers/pronunciation/word-bank";
import { addPronunciationFocus } from "@/lib/demo/demo-store";
import { getAIProvider } from "@/lib/providers";
import { getPrisma } from "@/lib/db";
import { isDemoMode } from "@/lib/config";
import { mergeWeaknessProfile, computeOverallFromFeedback } from "@/lib/scoring";
import type { FeedbackAnalysis } from "@/lib/schemas/feedback";
import { z } from "zod";

const bodySchema = z.object({
  type: z.string(),
  scenarioTitle: z.string(),
  durationSeconds: z.number(),
  transcripts: z.array(z.string()),
  analyses: z.array(z.record(z.string(), z.unknown())),
});

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (isDemoMode() || session.user.demo) {
    return NextResponse.json(getDemoProfile(session.user.email).sessions);
  }

  const prisma = await getPrisma();
  if (!prisma) return NextResponse.json(getDemoProfile(session.user.email).sessions);

  const sessions = await prisma.practiceSession.findMany({
    where: { userId: session.user.id },
    orderBy: { startedAt: "desc" },
    take: 20,
  });
  return NextResponse.json(sessions);
}

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = bodySchema.parse(await req.json());
  const analyses = body.analyses as unknown as FeedbackAnalysis[];
  const ai = getAIProvider();
  const summary = await ai.generateSessionSummary({
    transcripts: body.transcripts,
    analyses,
    scenario: body.scenarioTitle,
  });

  const last = analyses[analyses.length - 1];
  const overallScore = last ? computeOverallFromFeedback(last) : 70;
  const scorecard: Record<string, number> = last
    ? {
        fluency: last.fluency,
        grammar: last.grammar,
        vocabulary: last.vocabulary,
        clarity: last.clarity,
        confidence: last.confidence,
        conciseness: last.conciseness,
        leadership: last.leadership,
      }
    : { overall: overallScore };

  if (isDemoMode() || session.user.demo) {
    const newWords = body.transcripts.flatMap((t) => suggestWordsFromTranscript(t));
    if (newWords.length) upsertVocabulary(session.user.email, newWords);
    const pronounced = body.transcripts.flatMap((t) => detectWordsInTranscript(t));
    if (pronounced.length) addPronunciationFocus(session.user.email, pronounced.map((p) => p.word));
    const profile = getDemoProfile(session.user.email);
    profile.weaknessProfile = mergeWeaknessProfile(profile.weaknessProfile, last);
    if (last) {
      profile.communicationScores = {
        ...(profile.communicationScores as object),
        clarity: last.clarity,
        confidence: last.confidence,
      };
    }
    saveDemoProfile(profile);
    if (/leadership|challenge|disagreement/i.test(body.scenarioTitle + body.type)) {
      completeDailyChallenge(session.user.email, getDailyChallenge().id);
    }
    const saved = addDemoSession(session.user.email, {
      type: body.type,
      scenarioTitle: body.scenarioTitle,
      durationSeconds: body.durationSeconds,
      overallScore,
      scorecard,
      summary,
      startedAt: new Date().toISOString(),
    });
    return NextResponse.json({ session: saved, summary });
  }

  const prisma = await getPrisma();
  if (!prisma) {
    const saved = addDemoSession(session.user.email, {
      type: body.type,
      scenarioTitle: body.scenarioTitle,
      durationSeconds: body.durationSeconds,
      overallScore,
      scorecard,
      summary,
      startedAt: new Date().toISOString(),
    });
    return NextResponse.json({ session: saved, summary });
  }

  const practiceSession = await prisma.practiceSession.create({
    data: {
      userId: session.user.id,
      type: body.type,
      scenarioTitle: body.scenarioTitle,
      durationSeconds: body.durationSeconds,
      overallScore,
      scorecard,
      summary,
      endedAt: new Date(),
    },
  });

  return NextResponse.json({ session: practiceSession, summary });
}
