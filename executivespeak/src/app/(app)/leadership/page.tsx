import { ModuleScaffold } from "@/components/modules/module-scaffold";
import { SCENARIOS } from "@/lib/data/scenarios";

const LESSONS = [
  "Speak with authority without sounding arrogant",
  "Disagree professionally",
  "Give constructive feedback",
  "Push back professionally",
  "Run meetings",
  "Communicate bad news",
];

export default function LeadershipPage() {
  const scenarios = SCENARIOS.filter((s) => s.category === "leadership" || s.category === "meeting");
  return (
    <div className="space-y-8">
      <ModuleScaffold
        title="Lead Like a Communicator"
        description="Leadership communication training for engineers — realistic scenarios with speak-again feedback."
        scenarios={scenarios.map((s) => ({ slug: s.slug, title: s.title, prompt: s.prompt }))}
      />
      <div className="mx-auto max-w-4xl px-6 pb-10 lg:px-10">
        <h2 className="text-lg font-semibold">Lesson library</h2>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2 text-sm text-muted-foreground">
          {LESSONS.map((l) => (
            <li key={l} className="rounded-lg border px-3 py-2">
              {l}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
