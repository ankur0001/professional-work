import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getDemoProfile } from "@/lib/demo/demo-store";
import { computeWeeklyTrend } from "@/lib/analytics/weekly";
import { isDemoMode } from "@/lib/config";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (isDemoMode() || session.user.demo) {
    const profile = getDemoProfile(session.user.email);
    const trend = computeWeeklyTrend(profile.sessions);
    return NextResponse.json(trend);
  }

  return NextResponse.json({
    current: { weekStart: new Date().toISOString().slice(0, 10), sessionCount: 0 },
    previous: null,
    deltas: {},
  });
}
