import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import {
  getDemoProfile,
  reviewVocabularyWord,
  upsertVocabulary,
} from "@/lib/demo/demo-store";
import { isDemoMode } from "@/lib/config";
import { wordsDueForReview } from "@/lib/vocabulary/suggest";
import { z } from "zod";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  if (!isDemoMode() && !session.user.demo) {
    return NextResponse.json({ items: [], due: [] });
  }
  const profile = getDemoProfile(session.user.email);
  return NextResponse.json({
    items: profile.vocabularyItems,
    due: wordsDueForReview(profile.vocabularyItems),
  });
}

const postSchema = z.discriminatedUnion("action", [
  z.object({ action: z.literal("introduce"), words: z.array(z.string()) }),
  z.object({ action: z.literal("review"), word: z.string(), success: z.boolean() }),
]);

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = postSchema.parse(await req.json());
  if (isDemoMode() || session.user.demo) {
    if (body.action === "introduce") {
      upsertVocabulary(session.user.email, body.words);
    } else {
      reviewVocabularyWord(session.user.email, body.word, body.success);
    }
    const profile = getDemoProfile(session.user.email);
    return NextResponse.json({ items: profile.vocabularyItems });
  }
  return NextResponse.json({ ok: true });
}
