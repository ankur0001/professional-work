"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ProgressPage() {
  const [sessions, setSessions] = useState<{ scenarioTitle: string; overallScore: number; startedAt: string }[]>([]);

  useEffect(() => {
    fetch("/api/sessions")
      .then((r) => r.json())
      .then(setSessions)
      .catch(() => undefined);
  }, []);

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Progress</h1>
      <p className="text-sm text-muted-foreground">
        Trends are computed from your sessions only — we never fabricate improvement.
      </p>
      <div className="grid gap-3">
        {sessions.length === 0 && (
          <p className="text-muted-foreground">Complete a practice session to see history.</p>
        )}
        {sessions.map((s, i) => (
          <Card key={i}>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">{s.scenarioTitle}</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Score {s.overallScore} · {new Date(s.startedAt).toLocaleString()}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
