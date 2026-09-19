const UPGRADES: Record<string, string[]> = {
  good: ["effective", "valuable", "reliable", "scalable", "significant"],
  problem: ["issue", "constraint", "risk", "bottleneck", "trade-off"],
  bad: ["ineffective", "unreliable", "problematic"],
  big: ["significant", "substantial", "major"],
  small: ["minor", "limited", "narrow"],
};

export function suggestWordsFromTranscript(transcript: string): string[] {
  const lower = transcript.toLowerCase();
  const found: string[] = [];
  for (const [weak, alts] of Object.entries(UPGRADES)) {
    if (new RegExp(`\\b${weak}\\b`).test(lower)) {
      found.push(alts[0]);
    }
  }
  return [...new Set(found)];
}

export function wordsDueForReview(
  items: { word: string; dueAt: string; status: string }[],
  now = new Date(),
) {
  return items.filter((i) => i.status !== "mastered" && new Date(i.dueAt) <= now);
}
