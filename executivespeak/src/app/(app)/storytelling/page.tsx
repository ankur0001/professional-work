"use client";

import { useState } from "react";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { StoryAnalysis } from "@/lib/schemas/executive";

const PROMPTS = [
  "Tell me about a difficult project.",
  "Tell me about a failure.",
  "Tell me about a conflict.",
  "Tell me about a time you influenced someone.",
];

export default function StorytellingPage() {
  const [prompt, setPrompt] = useState(PROMPTS[0]);
  const [phase, setPhase] = useState<"speak" | "result">("speak");
  const [analysis, setAnalysis] = useState<StoryAnalysis | null>(null);

  if (phase === "speak") {
    return (
      <div>
        <div className="mx-auto max-w-3xl space-y-4 px-6 pt-8">
          <h1 className="text-3xl font-semibold">Storytelling trainer</h1>
          <p className="text-muted-foreground">Structure: Situation → Challenge → Action → Result → Lesson</p>
          <div className="flex flex-wrap gap-2">
            {PROMPTS.map((p) => (
              <Button key={p} size="sm" variant={p === prompt ? "default" : "outline"} onClick={() => setPrompt(p)}>
                {p.split(" ").slice(0, 3).join(" ")}…
              </Button>
            ))}
          </div>
        </div>
        <SpeakingSession
          scenarioTitle="Storytelling"
          initialPrompt={prompt}
          onComplete={async ({ transcripts }) => {
            const text = transcripts.join(" ");
            const res = await fetch("/api/story/analyze", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ transcript: text }),
            });
            setAnalysis(await res.json());
            setPhase("result");
          }}
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Story scorecard</h1>
      {analysis && (
        <>
          <div className="grid gap-3 sm:grid-cols-3">
            {(
              [
                ["Situation", analysis.situation],
                ["Challenge", analysis.challenge],
                ["Action", analysis.action],
                ["Result", analysis.result],
                ["Lesson", analysis.lesson],
                ["Overall", analysis.overall],
              ] as const
            ).map(([label, val]) => (
              <Card key={label}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">{label}</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold tabular-nums">{val}</CardContent>
              </Card>
            ))}
          </div>
          <Card>
            <CardContent className="space-y-2 pt-6 text-sm">
              <p>{analysis.structureNotes}</p>
              <p className="rounded-lg bg-muted/40 p-3">{analysis.improvedOutline}</p>
            </CardContent>
          </Card>
        </>
      )}
      <Button onClick={() => setPhase("speak")}>Tell another story</Button>
    </div>
  );
}
