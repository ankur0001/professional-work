export type ImpromptuCategory =
  | "Technology"
  | "Leadership"
  | "Career"
  | "Business"
  | "Workplace"
  | "Opinions";

export const IMPROMPTU_TOPICS: { category: ImpromptuCategory; topic: string }[] = [
  { category: "Technology", topic: "Should every team adopt microservices?" },
  { category: "Technology", topic: "What makes a good code review comment?" },
  { category: "Leadership", topic: "How do you influence without authority?" },
  { category: "Leadership", topic: "When should a tech lead escalate?" },
  { category: "Career", topic: "What separates a senior engineer from a mid-level engineer?" },
  { category: "Business", topic: "How do engineers contribute to revenue?" },
  { category: "Workplace", topic: "Is remote work better for deep technical work?" },
  { category: "Opinions", topic: "Will AI replace software engineers in five years?" },
  { category: "Workplace", topic: "How do you handle a teammate who misses deadlines?" },
  { category: "Technology", topic: "Why does technical debt accumulate?" },
];

export function randomImpromptuTopic(seed?: number) {
  const idx =
    seed !== undefined
      ? seed % IMPROMPTU_TOPICS.length
      : Math.floor(Math.random() * IMPROMPTU_TOPICS.length);
  return IMPROMPTU_TOPICS[idx];
}
