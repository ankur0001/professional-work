import { ModuleScaffold } from "@/components/modules/module-scaffold";

export default function InterviewPage() {
  return (
    <ModuleScaffold
      title="Interview coach"
      description="Technical and behavioral interview speaking practice."
      scenarios={[
        {
          slug: "warmup-yesterday",
          title: "Tell me about yourself",
          prompt: "Answer: Tell me about yourself.",
        },
        {
          slug: "tech-architecture-new-engineer",
          title: "Technical deep dive",
          prompt: "Describe a difficult technical problem you solved.",
        },
      ]}
    />
  );
}
