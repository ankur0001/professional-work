"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { getDailyPlan, getScenarioBySlug } from "@/lib/data/scenarios";

export function PracticeClient() {
  const params = useSearchParams();
  const router = useRouter();
  const mode = params.get("mode") ?? "standard";
  const slug = params.get("scenario");
  const plan = getDailyPlan(mode === "quick" ? 10 : mode === "deep" ? 30 : 20);
  const scenario = slug ? getScenarioBySlug(slug) : plan.items[3];
  const title = scenario?.title ?? "Architecture migration proposal";
  const prompt =
    scenario?.prompt ??
    "You're presenting a proposal to your manager. Explain why you want to migrate the service to a new architecture.";

  return (
    <SpeakingSession
      scenarioTitle={title}
      initialPrompt={prompt}
      personality="executive_coach"
      onComplete={async ({ transcripts, analyses, durationSeconds }) => {
        const res = await fetch("/api/sessions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            type: `practice_${mode}`,
            scenarioTitle: title,
            durationSeconds,
            transcripts,
            analyses,
          }),
        });
        const data = await res.json();
        sessionStorage.setItem("es_last_summary", JSON.stringify(data.summary));
        router.push("/practice/summary");
      }}
    />
  );
}
