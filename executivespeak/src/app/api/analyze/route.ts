import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getAIProvider } from "@/lib/providers";
import { z } from "zod";

const bodySchema = z.object({
  transcript: z.string().min(1),
  scenario: z.string(),
  personality: z.string().default("executive_coach"),
  mustEvaluateRepeat: z.string().optional(),
});

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid body" }, { status: 400 });
  }
  const ai = getAIProvider();
  const analysis = await ai.analyzeSpeech(parsed.data);
  return NextResponse.json(analysis);
}
