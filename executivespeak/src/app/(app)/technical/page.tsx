import { ModuleScaffold } from "@/components/modules/module-scaffold";

const TOPICS = [
  { slug: "tech-architecture-new-engineer", title: "Explain architecture", prompt: "Explain your current architecture to a new engineer." },
  { slug: "standup-blocker", title: "Standup blocker", prompt: "Explain a blocker clearly in standup." },
  { slug: "impromptu-tech-debt", title: "Technical debt", prompt: "Explain why technical debt matters." },
];

const TRAINER = [
  "REST API",
  "Microservices",
  "Kafka",
  "Kubernetes",
  "Database indexing",
  "OAuth",
  "CI/CD",
].map((t) => ({
  slug: "tech-architecture-new-engineer",
  title: `Explain ${t}`,
  prompt: `Explain ${t} to a junior engineer, then adapt for a product manager, then a CTO in 60 seconds.`,
}));

export default function TechnicalPage() {
  return (
    <ModuleScaffold
      title="Software Engineering English"
      description="Daily engineering conversations and technical explanation trainer with audience-aware coaching."
      scenarios={[...TOPICS, ...TRAINER.slice(0, 4)]}
    />
  );
}
