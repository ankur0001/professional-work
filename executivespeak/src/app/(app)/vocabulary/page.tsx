"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

interface VocabItem {
  word: string;
  status: string;
  dueAt: string;
  useCount: number;
}

export default function VocabularyPage() {
  const [items, setItems] = useState<VocabItem[]>([]);
  const [due, setDue] = useState<VocabItem[]>([]);

  async function load() {
    const res = await fetch("/api/vocabulary");
    const data = await res.json();
    setItems(data.items ?? []);
    setDue(data.due ?? []);
  }

  useEffect(() => {
    void load();
  }, []);

  async function review(word: string, success: boolean) {
    await fetch("/api/vocabulary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "review", word, success }),
    });
    await load();
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Vocabulary engine</h1>
      <p className="text-muted-foreground">
        Words are introduced from your real speech (e.g. upgrading &quot;good&quot; → scalable). Spaced repetition
        schedules reviews.
      </p>

      {due.length > 0 && (
        <Card className="border-primary/30">
          <CardHeader>
            <CardTitle className="text-base">Due for review</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {due.map((d) => (
              <div key={d.word} className="flex items-center justify-between gap-2">
                <span className="font-medium">{d.word}</span>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline" onClick={() => review(d.word, false)}>
                    Still learning
                  </Button>
                  <Button size="sm" onClick={() => review(d.word, true)}>
                    Used it well
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      <div className="grid gap-3">
        {items.map((item) => (
          <Card key={item.word}>
            <CardContent className="flex items-center justify-between pt-6">
              <div>
                <p className="font-medium">{item.word}</p>
                <p className="text-xs text-muted-foreground">Used {item.useCount} times in practice</p>
              </div>
              <Badge variant={item.status === "mastered" ? "default" : "secondary"}>{item.status}</Badge>
            </CardContent>
          </Card>
        ))}
      </div>

      <Button asChild variant="outline">
        <Link href="/practice">Practice using new words</Link>
      </Button>
    </div>
  );
}
