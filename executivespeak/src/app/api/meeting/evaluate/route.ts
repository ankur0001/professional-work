import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getAIProvider } from "@/lib/providers";
import { z } from "zod";

const schema = z.object({
  meetingTitle: z.string(),
  promptLine: z.string(),
  userResponse: z.string().min(1),
});

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = schema.parse(await req.json());
  const ai = getAIProvider();
  const result = await ai.evaluateMeetingResponse(body);
  return NextResponse.json(result);
}
