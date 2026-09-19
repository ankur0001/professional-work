import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { z } from "zod";
import { getPrisma } from "@/lib/db";
import { isDemoMode } from "@/lib/config";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(1),
});

export async function POST(req: Request) {
  if (isDemoMode()) {
    return NextResponse.json(
      { error: "Registration disabled in demo mode. Use demo@executivespeak.app / demo1234" },
      { status: 403 },
    );
  }
  const prisma = await getPrisma();
  if (!prisma) {
    return NextResponse.json({ error: "Database unavailable" }, { status: 503 });
  }
  const data = schema.parse(await req.json());
  const existing = await prisma.user.findUnique({ where: { email: data.email.toLowerCase() } });
  if (existing) {
    return NextResponse.json({ error: "Email already registered" }, { status: 409 });
  }
  const passwordHash = await bcrypt.hash(data.password, 10);
  const user = await prisma.user.create({
    data: {
      email: data.email.toLowerCase(),
      name: data.name,
      passwordHash,
      profile: { create: {} },
      coachSettings: { create: {} },
    },
  });
  return NextResponse.json({ id: user.id, email: user.email });
}
