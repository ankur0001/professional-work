"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type Summary = {
  strengths?: string[];
  improvements?: string[];
  topMistake?: string;
  betterPhrase?: string;
  tomorrowChallenge?: string;
};

export default function PracticeSummaryPage() {
  const [summary, setSummary] = useState<Summary>({});

  useEffect(() => {
    try {
      const raw = sessionStorage.getItem("es_last_summary");
      if (raw) setSummary(JSON.parse(raw));
    } catch {
      setSummary({});
    }
  }, []);

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Session summary</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">What you did well</CardTitle>
        </CardHeader>
        <CardContent className="list-disc space-y-1 pl-5 text-sm">
          {(summary.strengths ?? []).map((s) => (
            <li key={s}>{s}</li>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">What to improve</CardTitle>
        </CardHeader>
        <CardContent className="list-disc space-y-1 pl-5 text-sm">
          {(summary.improvements ?? []).map((s) => (
            <li key={s}>{s}</li>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardContent className="space-y-2 pt-6 text-sm">
          <p>
            <span className="font-medium">Most important mistake:</span> {summary.topMistake}
          </p>
          <p>
            <span className="font-medium">Better phrase:</span> {summary.betterPhrase}
          </p>
          <p>
            <span className="font-medium">Tomorrow:</span> {summary.tomorrowChallenge}
          </p>
        </CardContent>
      </Card>
      <Button asChild>
        <Link href="/dashboard">Back to dashboard</Link>
      </Button>
    </div>
  );
}
