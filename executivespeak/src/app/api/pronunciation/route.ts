import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getDemoProfile, addPronunciationFocus } from "@/lib/demo/demo-store";
import { detectWordsInTranscript, PRONUNCIATION_WORD_BANK } from "@/lib/providers/pronunciation/word-bank";
import { isDemoMode } from "@/lib/config";
import { z } from "zod";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (isDemoMode() || session.user.demo) {
    const profile = getDemoProfile(session.user.email);
    const focus = profile.pronunciationFocus
      .map((w) => PRONUNCIATION_WORD_BANK.find((e) => e.word === w))
      .filter(Boolean);
    return NextResponse.json({ focus, bank: PRONUNCIATION_WORD_BANK });
  }
  return NextResponse.json({ focus: PRONUNCIATION_WORD_BANK.slice(0, 3), bank: PRONUNCIATION_WORD_BANK });
}

const postSchema = z.object({
  transcript: z.string().optional(),
  word: z.string().optional(),
});

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = postSchema.parse(await req.json());

  if (body.transcript && (isDemoMode() || session.user.demo)) {
    const detected = detectWordsInTranscript(body.transcript);
    if (detected.length) {
      addPronunciationFocus(session.user.email, detected.map((d) => d.word));
    }
    return NextResponse.json({ detected });
  }

  const entry = PRONUNCIATION_WORD_BANK.find((e) => e.word === body.word);
  return NextResponse.json({ entry: entry ?? null });
}
