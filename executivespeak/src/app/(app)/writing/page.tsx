"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { WritingCoachResult } from "@/lib/schemas/writing";

export default function WritingCoachPage() {
  const [text, setText] = useState(
    "Hi, sorry to bother you — I think maybe we might need more time on this feature because there are some problems with the API.",
  );
  const [channel, setChannel] = useState<"slack" | "email" | "teams" | "jira" | "pr">("slack");
  const [result, setResult] = useState<WritingCoachResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);
    const res = await fetch("/api/writing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, channel }),
    });
    setResult(await res.json());
    setLoading(false);
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 lg:p-10">
      <div>
        <h1 className="text-3xl font-semibold">Email & chat coach</h1>
        <p className="mt-2 text-muted-foreground">Paste Slack, email, Teams, Jira, or PR comments.</p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Your message</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select
            className="rounded-lg border border-input bg-background p-2 text-sm"
            value={channel}
            onChange={(e) => setChannel(e.target.value as typeof channel)}
          >
            <option value="slack">Slack</option>
            <option value="email">Email</option>
            <option value="teams">Teams</option>
            <option value="jira">Jira</option>
            <option value="pr">PR comment</option>
          </select>
          <textarea
            className="min-h-[120px] w-full rounded-lg border border-input bg-background p-3 text-sm"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <Button onClick={analyze} disabled={loading}>
            {loading ? "Coaching…" : "Improve message"}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <div className="grid gap-4 md:grid-cols-2">
          {[
            ["Corrected", result.corrected],
            ["Natural", result.natural],
            ["Professional", result.professional],
            ["Leadership", result.leadership],
            ["Shorter", result.shorter],
            ["More confident", result.moreConfident],
            ["More diplomatic", result.moreDiplomatic],
            ["Executive-friendly", result.executiveFriendly],
          ].map(([label, val]) =>
            val ? (
              <Card key={label as string}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">{label}</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">{val}</CardContent>
              </Card>
            ) : null,
          )}
          <Card className="md:col-span-2">
            <CardContent className="space-y-2 pt-6 text-sm">
              <p>
                <span className="font-medium">Tone: </span>
                {result.toneNotes}
              </p>
              <p>
                <span className="font-medium">Clarity: </span>
                {result.clarityNotes}
              </p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
