"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function MistakesPage() {
  const [weaknesses, setWeaknesses] = useState<string[]>([]);

  useEffect(() => {
    fetch("/api/profile")
      .then((r) => r.json())
      .then((p) => {
        const w = p.weaknessProfile?.grammarWeaknesses ?? [];
        setWeaknesses(w);
      });
  }, []);

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Grammar memory</h1>
      <p className="text-muted-foreground">Recurring patterns from your speaking sessions.</p>
      {weaknesses.length === 0 ? (
        <p className="text-sm text-muted-foreground">No recurring mistakes tracked yet.</p>
      ) : (
        weaknesses.map((m) => (
          <Card key={m}>
            <CardContent className="pt-6 text-sm">{m}</CardContent>
          </Card>
        ))
      )}
    </div>
  );
}
