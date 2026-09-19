import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { introduceWords, listVocabulary, reviewWord } from "@/lib/services/vocabulary-service";
import { z } from "zod";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const data = await listVocabulary(session.user.id, session.user.email);
  return NextResponse.json(data);
}

const postSchema = z.discriminatedUnion("action", [
  z.object({ action: z.literal("introduce"), words: z.array(z.string()) }),
  z.object({ action: z.literal("review"), word: z.string(), success: z.boolean() }),
]);

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = postSchema.parse(await req.json());
  if (body.action === "introduce") {
    const items = await introduceWords(session.user.id, session.user.email, body.words);
    return NextResponse.json({ items });
  }
  const items = await reviewWord(session.user.id, session.user.email, body.word, body.success);
  return NextResponse.json({ items });
}
