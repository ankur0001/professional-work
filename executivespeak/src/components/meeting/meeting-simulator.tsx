"use client";

import { useState } from "react";
import { MEETING_SCRIPTS, type MeetingScript } from "@/lib/data/meetings";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { MeetingEvaluation } from "@/lib/schemas/writing";

function userTurnIndex(s: MeetingScript) {
  const idx = s.turns.findIndex((t) => t.afterUser);
  return idx >= 0 ? idx : s.turns.length - 1;
}

export function MeetingSimulator() {
  const [script, setScript] = useState<MeetingScript>(MEETING_SCRIPTS[0]);
  const [activeTurn, setActiveTurn] = useState(() => userTurnIndex(MEETING_SCRIPTS[0]));
  const [response, setResponse] = useState("");
  const [evaluation, setEvaluation] = useState<MeetingEvaluation | null>(null);
  const [loading, setLoading] = useState(false);

  const visibleTurns = script.turns.slice(0, activeTurn + 1);
  const awaitingUser = script.turns[activeTurn]?.afterUser ?? true;

  async function submitResponse() {
    if (!response.trim()) return;
    setLoading(true);
    const promptLine = script.turns[activeTurn].line;
    const res = await fetch("/api/meeting/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        meetingTitle: script.title,
        promptLine,
        userResponse: response,
      }),
    });
    const data = (await res.json()) as MeetingEvaluation;
    setEvaluation(data);
    setLoading(false);
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6 lg:p-10">
      <div>
        <h1 className="text-3xl font-semibold">Meeting simulator</h1>
        <p className="mt-2 text-muted-foreground">{script.context}</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {MEETING_SCRIPTS.map((s) => (
          <Button
            key={s.id}
            size="sm"
            variant={s.id === script.id ? "default" : "outline"}
            onClick={() => {
              setScript(s);
              setActiveTurn(userTurnIndex(s));
              setResponse("");
              setEvaluation(null);
            }}
          >
            {s.title}
          </Button>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Live meeting</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {visibleTurns.map((t, i) => (
            <div
              key={i}
              className={`rounded-lg px-3 py-2 text-sm ${
                t.speaker === "You" ? "ml-8 bg-primary/10" : "mr-4 bg-muted/50"
              }`}
            >
              <Badge variant="outline" className="mb-1">
                {t.speaker}
              </Badge>
              <p>{t.line}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      {awaitingUser && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Your response</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <textarea
              className="min-h-[100px] w-full rounded-lg border border-input bg-background p-3 text-sm"
              placeholder="Speak through your microphone in practice mode, or type your meeting response here…"
              value={response}
              onChange={(e) => setResponse(e.target.value)}
            />
            <Button onClick={submitResponse} disabled={loading}>
              {loading ? "Evaluating…" : "Submit response"}
            </Button>
          </CardContent>
        </Card>
      )}

      {evaluation && (
        <Card className="border-primary/30">
          <CardHeader>
            <CardTitle className="text-base">Meeting evaluation</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2 md:grid-cols-5">
              {(
                [
                  ["Clear", evaluation.clear],
                  ["Professional", evaluation.professional],
                  ["Assertive", evaluation.assertive],
                  ["Collaborative", evaluation.collaborative],
                  ["Leadership", evaluation.leadership],
                ] as const
              ).map(([label, val]) => (
                <div key={label} className="rounded-lg border p-2 text-center">
                  <p className="text-xs text-muted-foreground">{label}</p>
                  <p className="text-lg font-semibold tabular-nums">{val}</p>
                </div>
              ))}
            </div>
            <p>{evaluation.summary}</p>
            <p className="rounded-lg bg-muted/40 p-3">
              <span className="font-medium">Stronger version: </span>
              {evaluation.improvedVersion}
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
