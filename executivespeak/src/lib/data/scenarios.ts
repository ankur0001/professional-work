export type ScenarioCategory =
  | "warmup"
  | "technical"
  | "leadership"
  | "presentation"
  | "impromptu"
  | "reflection"
  | "meeting"
  | "interview";

export interface ScenarioDefinition {
  slug: string;
  title: string;
  category: ScenarioCategory;
  difficulty: number;
  prompt: string;
  description?: string;
}

export const SCENARIOS: ScenarioDefinition[] = [
  {
    slug: "warmup-yesterday",
    title: "Daily warm-up",
    category: "warmup",
    difficulty: 1,
    prompt: "Tell me what you worked on yesterday.",
  },
  {
    slug: "tech-architecture-new-engineer",
    title: "Explain architecture",
    category: "technical",
    difficulty: 2,
    prompt: "Explain your current architecture to a new engineer joining the team.",
  },
  {
    slug: "leadership-design-disagreement",
    title: "Design disagreement",
    category: "leadership",
    difficulty: 3,
    prompt: "Your teammate strongly disagrees with your design. Respond professionally and clearly.",
  },
  {
    slug: "presentation-90s",
    title: "90-second proposal",
    category: "presentation",
    difficulty: 3,
    prompt: "Explain your proposal to migrate a service to a new architecture in 90 seconds.",
  },
  {
    slug: "impromptu-tech-debt",
    title: "Impromptu: technical debt",
    category: "impromptu",
    difficulty: 2,
    prompt: "You have 60 seconds — explain why technical debt matters to your team.",
  },
  {
    slug: "reflection-difficulty",
    title: "Session reflection",
    category: "reflection",
    difficulty: 1,
    prompt: "What was difficult about today's conversation?",
  },
  {
    slug: "sprint-planning-lead",
    title: "Sprint planning",
    category: "meeting",
    difficulty: 3,
    prompt: "You are leading sprint planning. Set context and ask for estimates on the top priority item.",
  },
  {
    slug: "manager-pushback",
    title: "Manager pushback",
    category: "leadership",
    difficulty: 4,
    prompt: "Your manager says the migration timeline is too aggressive. Defend your plan without being defensive.",
  },
  {
    slug: "standup-blocker",
    title: "Standup blocker",
    category: "technical",
    difficulty: 2,
    prompt: "In standup, explain a blocker clearly and what you need from the team.",
  },
  {
    slug: "executive-60s-update",
    title: "Executive update",
    category: "presentation",
    difficulty: 4,
    prompt: "Give a 60-second executive update on your team's progress and risks.",
  },
];

export function getDailyPlan(minutes: number) {
  const items = [
    SCENARIOS.find((s) => s.slug === "warmup-yesterday")!,
    SCENARIOS.find((s) => s.slug === "tech-architecture-new-engineer")!,
    SCENARIOS.find((s) => s.slug === "leadership-design-disagreement")!,
    SCENARIOS.find((s) => s.slug === "presentation-90s")!,
    SCENARIOS.find((s) => s.slug === "impromptu-tech-debt")!,
    SCENARIOS.find((s) => s.slug === "reflection-difficulty")!,
  ];
  return {
    minutes,
    focus: "Speaking with more clarity and authority",
    challenge: "Explain a technical decision to a non-technical manager in 60 seconds.",
    items: items.map((s, i) => ({
      order: i + 1,
      type: s.category,
      title: s.title,
      prompt: s.prompt,
      slug: s.slug,
    })),
  };
}

export function getScenarioBySlug(slug: string) {
  return SCENARIOS.find((s) => s.slug === slug);
}
