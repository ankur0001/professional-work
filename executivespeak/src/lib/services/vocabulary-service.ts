import { getPrisma } from "@/lib/db";
import { isDemoMode } from "@/lib/config";
import {
  getDemoProfile,
  reviewVocabularyWord,
  upsertVocabulary,
  type VocabularyEntry,
} from "@/lib/demo/demo-store";
import { wordsDueForReview } from "@/lib/vocabulary/suggest";

export async function listVocabulary(userId: string, email: string) {
  if (isDemoMode()) {
    const profile = getDemoProfile(email);
    return {
      items: profile.vocabularyItems,
      due: wordsDueForReview(profile.vocabularyItems),
    };
  }

  const prisma = await getPrisma();
  if (!prisma) {
    const profile = getDemoProfile(email);
    return { items: profile.vocabularyItems, due: wordsDueForReview(profile.vocabularyItems) };
  }

  const items = await prisma.vocabularyItem.findMany({
    where: { userId },
    orderBy: { introducedAt: "desc" },
  });
  const mapped: VocabularyEntry[] = items.map((i) => ({
    word: i.word,
    introducedAt: i.introducedAt.toISOString(),
    dueAt: i.lastUsedAt?.toISOString() ?? i.introducedAt.toISOString(),
    useCount: i.useCount,
    status: i.status as VocabularyEntry["status"],
  }));
  return { items: mapped, due: wordsDueForReview(mapped) };
}

export async function introduceWords(userId: string, email: string, words: string[]) {
  if (isDemoMode()) {
    upsertVocabulary(email, words);
    return getDemoProfile(email).vocabularyItems;
  }
  const prisma = await getPrisma();
  if (!prisma) {
    upsertVocabulary(email, words);
    return getDemoProfile(email).vocabularyItems;
  }
  for (const word of words) {
    await prisma.vocabularyItem.upsert({
      where: { userId_word: { userId, word } },
      create: { userId, word, context: "From speaking session" },
      update: {},
    });
  }
  const items = await prisma.vocabularyItem.findMany({ where: { userId } });
  return items.map((i) => ({
    word: i.word,
    introducedAt: i.introducedAt.toISOString(),
    dueAt: i.introducedAt.toISOString(),
    useCount: i.useCount,
    status: i.status as VocabularyEntry["status"],
  }));
}

export async function reviewWord(userId: string, email: string, word: string, success: boolean) {
  if (isDemoMode()) {
    reviewVocabularyWord(email, word, success);
    return getDemoProfile(email).vocabularyItems;
  }
  const prisma = await getPrisma();
  if (!prisma) {
    reviewVocabularyWord(email, word, success);
    return getDemoProfile(email).vocabularyItems;
  }
  const item = await prisma.vocabularyItem.findUnique({
    where: { userId_word: { userId, word } },
  });
  if (item) {
    await prisma.vocabularyItem.update({
      where: { id: item.id },
      data: {
        useCount: success ? item.useCount + 1 : item.useCount,
        status: success && item.useCount + 1 >= 3 ? "mastered" : "review",
        lastUsedAt: new Date(),
      },
    });
    await prisma.vocabularyReview.create({
      data: {
        userId,
        vocabularyItemId: item.id,
        dueAt: new Date(Date.now() + (success ? 7 : 1) * 86400000),
        completedAt: new Date(),
        success,
      },
    });
  }
  return (await listVocabulary(userId, email)).items;
}
