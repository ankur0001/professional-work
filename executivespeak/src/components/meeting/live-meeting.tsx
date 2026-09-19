"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { MeetingTurn } from "@/lib/schemas/executive";
import type { MeetingEvaluation } from "@/lib/schemas/writing";

async function requestTurn(
  history: { speaker: string; line: string }[],
  userResponse?: string,
): Promise<MeetingTurn> {
  const res = await fetch("/api/meeting/turn", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      meetingId: "sprint-deadline-live",
      history,
      userResponse,
    }),
  });
  return res.json();
}

export function LiveMeeting() {
  const [history, setHistory] = useState<{ speaker: string; line: string }[]>([]);
  const [response, setResponse] = useState("");
  const [evaluation, setEvaluation] = useState<MeetingEvaluation | null>(null);
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const [expectsResponse, setExpectsResponse] = useState(false);

  async function startMeeting() {
    setLoading(true);
    setStarted(true);
    setEvaluation(null);
    let h: { speaker: string; line: string }[] = [];
    for (let i = 0; i < 2; i++) {
      const turn = await requestTurn(h);
      h = [...h, { speaker: turn.speaker, line: turn.line }];
    }
    setHistory(h);
    setExpectsResponse(true);
    setLoading(false);
  }

  async function submitResponse() {
    if (!response.trim()) return;
    setLoading(true);
    const line = response;
    const hWithUser = [...history, { speaker: "You", line }];
    setHistory(hWithUser);
    setResponse("");
    const evalRes = await fetch("/api/meeting/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        meetingTitle: "Live sprint planning",
        promptLine: history[history.length - 1]?.line ?? "",
        userResponse: line,
      }),
    });
    setEvaluation(await evalRes.json());
    const turn = await requestTurn(hWithUser, line);
    setHistory((prev) => [...prev, { speaker: turn.speaker, line: turn.line }]);
    setExpectsResponse(turn.expectsUserResponse);
    setLoading(false);
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 px-6 pt-10">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">Live multi-agent meeting</h2>
          <p className="text-sm text-muted-foreground">PM, Engineer, and Manager respond dynamically to you.</p>
        </div>
        {!started && (
          <Button onClick={startMeeting} disabled={loading}>
            Start live meeting
          </Button>
        )}
      </div>

      {started && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Participants</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {history.map((t, i) => (
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
      )}

      {started && expectsResponse && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Your response</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <textarea
              className="min-h-[100px] w-full rounded-lg border border-input bg-background p-3 text-sm"
              value={response}
              onChange={(e) => setResponse(e.target.value)}
            />
            <Button onClick={submitResponse} disabled={loading}>
              Respond & continue meeting
            </Button>
          </CardContent>
        </Card>
      )}

      {evaluation && (
        <Card className="border-primary/30">
          <CardContent className="pt-6 text-sm">
            <p className="font-medium">Latest evaluation — Leadership: {evaluation.leadership}/100</p>
            <p className="mt-2 text-muted-foreground">{evaluation.summary}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
