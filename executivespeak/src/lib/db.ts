import { isDemoMode } from "@/lib/config";

type PrismaClient = import("@/generated/prisma/client").PrismaClient;

let prisma: PrismaClient | null = null;

export async function getPrisma(): Promise<PrismaClient | null> {
  if (isDemoMode()) return null;
  if (prisma) return prisma;
  try {
    const { PrismaClient } = await import("@/generated/prisma/client");
    const { PrismaPg } = await import("@prisma/adapter-pg");
    const connectionString = process.env.DATABASE_URL;
    if (!connectionString) return null;
    const adapter = new PrismaPg({ connectionString });
    prisma = new PrismaClient({ adapter });
    await prisma.$connect();
    return prisma;
  } catch {
    return null;
  }
}

export async function disconnectPrisma() {
  if (prisma) {
    await prisma.$disconnect();
    prisma = null;
  }
}
