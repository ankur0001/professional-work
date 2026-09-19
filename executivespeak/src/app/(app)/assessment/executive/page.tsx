"use client";

import { useEffect, useState } from "react";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { ExecutiveReport } from "@/lib/schemas/executive";
import Link from "next/link";

const SCENARIO =
  "You are a senior engineer presenting a major technical decision to the CTO. Explain why the team should migrate to event-driven architecture, including business impact, risks, and your recommendation.";

export default function ExecutiveAssessmentPage() {
  const [phase, setPhase] = useState<"intro" | "speak" | "report">("intro");
  const [report, setReport] = useState<ExecutiveReport | null>(null);
  const [saved, setSaved] = useState<ExecutiveReport | null>(null);

  useEffect(() => {
    fetch("/api/assessments/executive")
      .then((r) => r.json())
      .then((d) => setSaved(d.report as ExecutiveReport | null));
  }, []);

  if (phase === "intro") {
    return (
      <div className="mx-auto max-w-2xl space-y-6 p-8">
        <h1 className="text-3xl font-semibold">Executive Communication Day</h1>
        <p className="text-muted-foreground">
          Monthly assessment (~10 minutes). Coaching metrics only — not a standardized language test.
        </p>
        {saved && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">This month&apos;s report on file</CardTitle>
            </CardHeader>
            <CardContent className="text-sm">Overall: {saved.overall}/100 — you may retake to improve.</CardContent>
          </Card>
        )}
        <Button size="lg" onClick={() => setPhase("speak")}>
          Begin executive presentation
        </Button>
        <Button asChild variant="ghost">
          <Link href="/assessment">Back to weekly assessment</Link>
        </Button>
      </div>
    );
  }

  if (phase === "speak") {
    return (
      <SpeakingSession
        scenarioTitle="Executive Communication Day"
        initialPrompt={SCENARIO}
        personality="cto"
        onComplete={async ({ transcripts }) => {
          const res = await fetch("/api/assessments/executive", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ transcripts, scenario: SCENARIO }),
          });
          setReport(await res.json());
          setPhase("report");
        }}
      />
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Executive coaching report</h1>
      {report && (
        <>
          <div className="grid gap-3 sm:grid-cols-3">
            {Object.entries(report)
              .filter(([k]) => k !== "coachingReport" && k !== "topThreeActions")
              .map(([k, v]) => (
                <Card key={k}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs capitalize">{k.replace(/([A-Z])/g, " $1")}</CardTitle>
                  </CardHeader>
                  <CardContent className="text-xl font-semibold tabular-nums">{v as number}</CardContent>
                </Card>
              ))}
          </div>
          <Card>
            <CardContent className="space-y-3 pt-6 text-sm">
              <p>{report.coachingReport}</p>
              <ul className="list-disc space-y-1 pl-5">
                {report.topThreeActions.map((a) => (
                  <li key={a}>{a}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </>
      )}
      <Button asChild>
        <Link href="/dashboard">Back to dashboard</Link>
      </Button>
    </div>
  );
}
