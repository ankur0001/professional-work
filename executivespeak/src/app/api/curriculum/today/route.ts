import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getDemoProfile } from "@/lib/demo/demo-store";
import { buildPersonalizedPlan } from "@/lib/curriculum/personalize";
import { getPrisma } from "@/lib/db";
import { isDemoMode } from "@/lib/config";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (isDemoMode() || session.user.demo) {
    const profile = getDemoProfile(session.user.email);
    return NextResponse.json(buildPersonalizedPlan(profile));
  }

  const prisma = await getPrisma();
  if (!prisma) {
    return NextResponse.json(buildPersonalizedPlan(getDemoProfile(session.user.email)));
  }

  const profile = await prisma.userProfile.findUnique({ where: { userId: session.user.id } });
  return NextResponse.json(
    buildPersonalizedPlan({
      dailyPracticeMinutes: profile?.dailyPracticeMinutes ?? 20,
      communicationScores: (profile?.communicationScores as Record<string, number>) ?? {},
      weaknessProfile: (profile?.weaknessProfile as object) ?? {},
    }),
  );
}
