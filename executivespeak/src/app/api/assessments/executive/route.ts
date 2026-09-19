import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth-options";
import { getAIProvider } from "@/lib/providers";
import { saveMonthlyReport } from "@/lib/demo/demo-store";
import { isDemoMode } from "@/lib/config";
import { getPrisma } from "@/lib/db";
import { z } from "zod";

const schema = z.object({
  transcripts: z.array(z.string()).min(1),
  scenario: z.string(),
});

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const body = schema.parse(await req.json());
  const ai = getAIProvider();
  const report = await ai.analyzeExecutivePresentation(body);
  const monthStart = new Date().toISOString().slice(0, 7) + "-01";

  if (isDemoMode() || session.user.demo) {
    saveMonthlyReport(session.user.email, monthStart, report as unknown as Record<string, unknown>);
  } else {
    const prisma = await getPrisma();
    if (prisma) {
      await prisma.monthlyAssessment.upsert({
        where: {
          userId_monthStart: {
            userId: session.user.id,
            monthStart: new Date(monthStart),
          },
        },
        create: {
          userId: session.user.id,
          monthStart: new Date(monthStart),
          report,
        },
        update: { report },
      });
    }
  }

  return NextResponse.json(report);
}

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  const monthStart = new Date().toISOString().slice(0, 7) + "-01";

  if (isDemoMode() || session.user.demo) {
    const { getDemoProfile } = await import("@/lib/demo/demo-store");
    const found = getDemoProfile(session.user.email).monthlyReports.find(
      (m) => m.monthStart === monthStart,
    );
    return NextResponse.json({ report: found?.report ?? null, monthStart });
  }

  const prisma = await getPrisma();
  if (!prisma) return NextResponse.json({ report: null, monthStart });
  const row = await prisma.monthlyAssessment.findUnique({
    where: {
      userId_monthStart: { userId: session.user.id, monthStart: new Date(monthStart) },
    },
  });
  return NextResponse.json({ report: row?.report ?? null, monthStart });
}
