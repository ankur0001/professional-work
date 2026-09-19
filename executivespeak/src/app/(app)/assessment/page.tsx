"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { WeeklyTrend } from "@/lib/analytics/weekly";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function AssessmentPage() {
  const [trend, setTrend] = useState<WeeklyTrend | null>(null);

  useEffect(() => {
    fetch("/api/assessments/weekly")
      .then((r) => r.json())
      .then(setTrend);
  }, []);

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-3xl font-semibold">Weekly assessment</h1>
        <Button asChild variant="outline">
          <Link href="/assessment/executive">Monthly executive day</Link>
        </Button>
      </div>
      <p className="text-sm text-muted-foreground">
        Trends are calculated from your actual sessions only — never fabricated.
      </p>
      {!trend ? (
        <p className="text-muted-foreground">Loading…</p>
      ) : trend.current.sessionCount === 0 ? (
        <Card>
          <CardContent className="pt-6 text-sm">
            Complete speaking sessions this week to unlock week-over-week trends.
            <Button asChild className="mt-4">
              <Link href="/practice">Start practice</Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">This week</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-2 text-sm sm:grid-cols-2">
              <p>Sessions: {trend.current.sessionCount}</p>
              <p>Speaking minutes: {trend.current.speakingMinutes}</p>
              <p>Avg score: {trend.current.avgOverallScore}</p>
              <p>Avg clarity: {trend.current.avgClarity}</p>
              <p>Avg leadership: {trend.current.avgLeadership}</p>
            </CardContent>
          </Card>
          {trend.previous && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Week over week</CardTitle>
              </CardHeader>
              <CardContent className="space-y-1 text-sm">
                {Object.entries(trend.deltas).map(([k, v]) =>
                  v !== null ? (
                    <p key={k}>
                      {k}: {v > 0 ? "+" : ""}
                      {v}
                    </p>
                  ) : null,
                )}
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
