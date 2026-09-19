import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getAIProvider } from "@/lib/providers";
import { z } from "zod";

const schema = z.object({
  meetingId: z.string(),
  history: z.array(z.object({ speaker: z.string(), line: z.string() })),
  userResponse: z.string().optional(),
});

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = schema.parse(await req.json());
  const ai = getAIProvider();
  const turn = await ai.generateMeetingTurn(body);
  return NextResponse.json(turn);
}
