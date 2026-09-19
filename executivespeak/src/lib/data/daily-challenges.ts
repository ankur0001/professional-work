export const LEADERSHIP_CHALLENGES = [
  {
    id: "disagree-no-defensive",
    title: "Explain a disagreement without sounding defensive",
    prompt: "Your PM rejected your estimate. Explain your reasoning calmly and propose a path forward.",
  },
  {
    id: "constructive-feedback",
    title: "Give constructive feedback",
    prompt: "A junior engineer merged code with weak tests. Give feedback that is direct and supportive.",
  },
  {
    id: "say-no-deadline",
    title: "Say no to an unrealistic deadline",
    prompt: "Leadership wants a feature by Friday. Push back professionally and offer alternatives.",
  },
  {
    id: "risk-non-technical",
    title: "Explain technical risk to a non-technical stakeholder",
    prompt: "Explain why skipping load testing before launch is risky — in plain language.",
  },
  {
    id: "prioritize-tech-debt",
    title: "Convince your manager to prioritize technical debt",
    prompt: "Make the business case for dedicating 20% of sprint capacity to tech debt.",
  },
  {
    id: "60s-update",
    title: "Give a 60-second project update",
    prompt: "Update your engineering manager: progress, blockers, and next steps in under 60 seconds.",
  },
];

export function getDailyChallenge(date = new Date()) {
  const dayIndex = Math.floor(date.getTime() / 86_400_000) % LEADERSHIP_CHALLENGES.length;
  return LEADERSHIP_CHALLENGES[dayIndex];
}
