export interface GrammarDrill {
  id: string;
  wrong: string;
  correct: string;
  prompt: string;
}

export function drillsFromWeaknesses(weaknesses: string[]): GrammarDrill[] {
  const defaults: GrammarDrill[] = [
    {
      id: "he-doesnt",
      wrong: "He don't agree",
      correct: "He doesn't agree",
      prompt: "Say: He doesn't agree with the timeline.",
    },
    {
      id: "past-simple",
      wrong: "Yesterday I have worked",
      correct: "Yesterday I worked",
      prompt: "Say: Yesterday I worked on the migration.",
    },
  ];
  const fromProfile = weaknesses.slice(0, 5).map((w, i) => {
    const parts = w.split("→").map((s) => s.trim());
    return {
      id: `custom-${i}`,
      wrong: parts[0] ?? w,
      correct: parts[1] ?? w,
      prompt: `Avoid "${parts[0]}". Say the corrected form in a full sentence.`,
    };
  });
  return [...fromProfile, ...defaults].slice(0, 6);
}
