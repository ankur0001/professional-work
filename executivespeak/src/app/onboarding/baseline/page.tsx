"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
const BASELINE_QUESTIONS = [
  "Tell me about yourself.",
  "Explain your current project.",
  "Describe a difficult technical problem you solved.",
  "Explain a disagreement you had with a teammate.",
  "What would you change in your current engineering process?",
  "Give your opinion on remote work or AI in software engineering.",
];

export default function BaselinePage() {
  const router = useRouter();
  const [qIndex, setQIndex] = useState(0);
  const [transcripts, setTranscripts] = useState<string[]>([]);
  const [done, setDone] = useState(false);
  const [scores, setScores] = useState<Record<string, number> | null>(null);

  async function completeBaseline(allTranscripts: string[]) {
    const res = await fetch("/api/baseline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcripts: allTranscripts }),
    });
    const data = await res.json();
    setScores(data);
    await fetch("/api/profile", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        communicationScores: data,
        baselineCompleted: true,
        onboardingCompleted: true,
      }),
    });
    setDone(true);
  }

  if (done && scores) {
    return (
      <div className="mx-auto max-w-2xl space-y-6 p-8">
        <h1 className="text-3xl font-semibold">Your communication profile</h1>
        <p className="text-sm text-muted-foreground">
          Internal coaching baseline — not an absolute scientific measurement.
        </p>
        <div className="grid gap-3 sm:grid-cols-2">
          {Object.entries(scores).map(([k, v]) => (
            <Card key={k}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm capitalize">{k.replace(/([A-Z])/g, " $1")}</CardTitle>
              </CardHeader>
              <CardContent className="text-2xl font-semibold tabular-nums">{v}/100</CardContent>
            </Card>
          ))}
        </div>
        <Button onClick={() => router.push("/dashboard")}>Go to dashboard</Button>
      </div>
    );
  }

  const prompt = BASELINE_QUESTIONS[qIndex];

  return (
    <SpeakingSession
      scenarioTitle={`Baseline · Question ${qIndex + 1}/${BASELINE_QUESTIONS.length}`}
      initialPrompt={prompt}
      onComplete={({ transcripts: ts }) => {
        const next = [...transcripts, ...ts];
        setTranscripts(next);
        if (qIndex + 1 < BASELINE_QUESTIONS.length) {
          setQIndex((i) => i + 1);
        } else {
          void completeBaseline(next);
        }
      }}
    />
  );
}
