import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getDailyChallenge } from "@/lib/data/daily-challenges";
import { completeDailyChallenge, getDemoProfile } from "@/lib/demo/demo-store";
import { isDemoMode } from "@/lib/config";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const challenge = getDailyChallenge();
  let completed = false;
  if (isDemoMode() || session.user.demo) {
    const profile = getDemoProfile(session.user.email);
    completed = profile.completedChallengeIds.includes(challenge.id);
  }
  return NextResponse.json({ challenge, completed });
}

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const { challengeId } = (await req.json()) as { challengeId: string };
  if (isDemoMode() || session.user.demo) {
    completeDailyChallenge(session.user.email, challengeId);
  }
  return NextResponse.json({ ok: true });
}
