import bcrypt from "bcryptjs";

async function main() {
  const { PrismaClient } = await import("../src/generated/prisma/client");
  const prisma = new PrismaClient();

  const email = "coach@executivespeak.app";
  const passwordHash = await bcrypt.hash("changeme123", 10);

  const user = await prisma.user.upsert({
    where: { email },
    update: {},
    create: {
      email,
      name: "Seed User",
      passwordHash,
      profile: {
        create: {
          profession: "Software Engineer",
          onboardingCompleted: true,
          baselineCompleted: true,
          currentLevel: 4,
          currentLevelLabel: "Professional Communicator",
          communicationScores: {
            speakingFluency: 62,
            grammar: 68,
            vocabulary: 55,
            clarity: 58,
            confidence: 61,
          },
          weaknessProfile: { fillerWords: ["basically"] },
        },
      },
      coachSettings: { create: {} },
    },
  });

  const scenarios = [
    {
      slug: "presentation-90s",
      title: "90-second proposal",
      category: "presentation",
      difficulty: 3,
      prompt: "Explain your proposal in 90 seconds.",
    },
    {
      slug: "leadership-design-disagreement",
      title: "Design disagreement",
      category: "leadership",
      difficulty: 3,
      prompt: "Your teammate strongly disagrees with your design.",
    },
  ];

  for (const s of scenarios) {
    await prisma.scenario.upsert({
      where: { slug: s.slug },
      update: s,
      create: s,
    });
  }

  const achievements = [
    { slug: "first_conversation", title: "First Conversation", description: "Complete your first speaking session" },
    { slug: "ten_minutes", title: "10 Minutes Spoken", description: "Speak for 10 cumulative minutes" },
  ];

  for (const a of achievements) {
    await prisma.achievement.upsert({
      where: { slug: a.slug },
      update: a,
      create: a,
    });
  }

  console.log("Seeded user:", user.email);
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
