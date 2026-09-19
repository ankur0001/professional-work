import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getDemoProfile, saveDemoProfile, updateDemoProfile } from "@/lib/demo/demo-store";
import { getPrisma } from "@/lib/db";
import { isDemoMode } from "@/lib/config";
import { z } from "zod";
import { LEVEL_LABELS, levelFromScores } from "@/lib/scoring";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (isDemoMode() || session.user.demo) {
    return NextResponse.json(getDemoProfile(session.user.email));
  }

  const prisma = await getPrisma();
  if (!prisma) {
    return NextResponse.json(getDemoProfile(session.user.email));
  }

  const profile = await prisma.userProfile.findUnique({
    where: { userId: session.user.id },
  });
  if (!profile) {
    return NextResponse.json({ onboardingCompleted: false });
  }
  return NextResponse.json(profile);
}

const patchSchema = z.object({
  name: z.string().optional(),
  profession: z.string().optional(),
  yearsExperience: z.coerce.number().optional(),
  englishLevel: z.string().optional(),
  nativeLanguage: z.string().optional(),
  targetAccent: z.string().optional(),
  dailyPracticeMinutes: z.coerce.number().optional(),
  primaryGoal: z.string().optional(),
  confidenceScore: z.coerce.number().optional(),
  communicationProblems: z.array(z.string()).optional(),
  onboardingCompleted: z.boolean().optional(),
  baselineCompleted: z.boolean().optional(),
  communicationScores: z.record(z.string(), z.number()).optional(),
  coachPersonality: z.string().optional(),
});

export async function PATCH(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const body = patchSchema.parse(await req.json());

  if (isDemoMode() || session.user.demo) {
    const updated = updateDemoProfile(session.user.email, body as Parameters<typeof updateDemoProfile>[1]);
    if (body.communicationScores) {
      const level = levelFromScores(body.communicationScores);
      updated.currentLevel = level;
      updated.currentLevelLabel = LEVEL_LABELS[level];
      saveDemoProfile(updated);
    }
    return NextResponse.json(updated);
  }

  const prisma = await getPrisma();
  if (!prisma) {
    return NextResponse.json(updateDemoProfile(session.user.email, body as Parameters<typeof updateDemoProfile>[1]));
  }

  const scores = body.communicationScores;
  let levelUpdate = {};
  if (scores) {
    const level = levelFromScores(scores);
    levelUpdate = { currentLevel: level, currentLevelLabel: LEVEL_LABELS[level] };
  }

  const profile = await prisma.userProfile.upsert({
    where: { userId: session.user.id },
    create: {
      userId: session.user.id,
      ...body,
      weaknessProfile: {},
      ...levelUpdate,
    },
    update: { ...body, ...levelUpdate },
  });
  return NextResponse.json(profile);
}
