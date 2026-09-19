"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { drillsFromWeaknesses, type GrammarDrill } from "@/lib/grammar/drills";

export default function MistakesPage() {
  const [weaknesses, setWeaknesses] = useState<string[]>([]);
  const [drills, setDrills] = useState<GrammarDrill[]>([]);

  useEffect(() => {
    fetch("/api/profile")
      .then((r) => r.json())
      .then((p) => {
        const w = p.weaknessProfile?.grammarWeaknesses ?? [];
        setWeaknesses(w);
        setDrills(drillsFromWeaknesses(w));
      });
  }, []);

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Grammar memory</h1>
      <p className="text-muted-foreground">Recurring patterns from your sessions — with targeted speak-aloud drills.</p>

      {weaknesses.length === 0 ? (
        <p className="text-sm text-muted-foreground">Complete a practice session to track recurring mistakes.</p>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recurring issues</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            {weaknesses.map((m) => (
              <p key={m} className="rounded-lg bg-muted/40 px-3 py-2">
                {m}
              </p>
            ))}
          </CardContent>
        </Card>
      )}

      <div className="space-y-3">
        <h2 className="text-lg font-semibold">Targeted drills</h2>
        {drills.map((d) => (
          <Card key={d.id}>
            <CardContent className="space-y-2 pt-6 text-sm">
              <p>
                <span className="text-destructive line-through">{d.wrong}</span>
              </p>
              <p className="text-primary">✓ {d.correct}</p>
              <p className="text-muted-foreground">{d.prompt}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Button asChild>
        <Link href="/practice">Speak the corrected forms</Link>
      </Button>
    </div>
  );
}
