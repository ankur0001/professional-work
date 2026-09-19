export interface MeetingScript {
  id: string;
  title: string;
  context: string;
  participants: string[];
  turns: { speaker: string; line: string; afterUser?: boolean }[];
  evaluationCriteria: string[];
}

export const MEETING_SCRIPTS: MeetingScript[] = [
  {
    id: "sprint-deadline",
    title: "Sprint planning — deadline push",
    context: "You are the tech lead. PM wants an aggressive date.",
    participants: ["Product Manager", "Engineer", "You"],
    turns: [
      {
        speaker: "Product Manager",
        line: "We need this feature by Friday. Marketing already announced it.",
      },
      {
        speaker: "Engineer",
        line: "That timeline isn't realistic. We still have integration testing open.",
      },
      {
        speaker: "Product Manager",
        line: "Can we cut scope or add people?",
        afterUser: true,
      },
    ],
    evaluationCriteria: ["Clear", "Professional", "Assertive", "Collaborative", "Leadership-level"],
  },
  {
    id: "incident-review",
    title: "Production incident review",
    context: "Post-incident meeting. Stay factual and forward-looking.",
    participants: ["Engineering Manager", "QA", "You"],
    turns: [
      {
        speaker: "Engineering Manager",
        line: "Walk us through what happened during yesterday's outage.",
      },
      {
        speaker: "QA",
        line: "Why didn't our alerts catch this earlier?",
        afterUser: true,
      },
    ],
    evaluationCriteria: ["Clear", "Professional", "Accountable", "Structured"],
  },
];
