import { ModuleScaffold } from "@/components/modules/module-scaffold";

export default function PresentationPage() {
  return (
    <ModuleScaffold
      title="Presentation Studio"
      description="Timed presentations with structure, filler, and executive clarity feedback."
      scenarios={[
        {
          slug: "presentation-90s",
          title: "90-second proposal",
          prompt: "Explain your proposal in 90 seconds.",
        },
        {
          slug: "executive-60s-update",
          title: "Executive update",
          prompt: "Give a 60-second executive project update.",
        },
      ]}
    />
  );
}
