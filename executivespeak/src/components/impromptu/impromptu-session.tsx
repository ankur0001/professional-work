"use client";

import { useEffect, useState } from "react";
import { randomImpromptuTopic } from "@/lib/data/impromptu-topics";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type Phase = "setup" | "think" | "speak" | "done";

export function ImpromptuSession() {
  const [topic] = useState(() => randomImpromptuTopic());
  const [speakSeconds, setSpeakSeconds] = useState(60);
  const [phase, setPhase] = useState<Phase>("setup");
  const [thinkLeft, setThinkLeft] = useState(15);

  useEffect(() => {
    if (phase !== "think") return;
    if (thinkLeft <= 0) {
      setPhase("speak");
      return;
    }
    const t = window.setTimeout(() => setThinkLeft((s) => s - 1), 1000);
    return () => window.clearTimeout(t);
  }, [phase, thinkLeft]);

  if (phase === "speak") {
    return (
      <SpeakingSession
        scenarioTitle={`Impromptu · ${speakSeconds}s`}
        initialPrompt={`${topic.topic} — you have ${speakSeconds} seconds.`}
        personality="native_speaker"
        onComplete={() => setPhase("done")}
      />
    );
  }

  if (phase === "done") {
    return (
      <div className="mx-auto max-w-xl p-10 text-center">
        <h2 className="text-2xl font-semibold">Impromptu complete</h2>
        <p className="mt-2 text-muted-foreground">Review your feedback above, then try another topic.</p>
        <Button className="mt-6" onClick={() => window.location.reload()}>
          New topic
        </Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Impromptu speaking</h1>
      <Card>
        <CardHeader>
          <Badge>{topic.category}</Badge>
          <CardTitle className="text-lg">{topic.topic}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">Choose speaking time after a 15-second think period.</p>
          <div className="flex flex-wrap gap-2">
            {[30, 60, 90].map((s) => (
              <Button
                key={s}
                variant={speakSeconds === s ? "default" : "outline"}
                size="sm"
                onClick={() => setSpeakSeconds(s)}
              >
                {s}s
              </Button>
            ))}
          </div>
          {phase === "think" ? (
            <p className="text-center text-4xl font-semibold tabular-nums">{thinkLeft}</p>
          ) : (
            <Button className="w-full" onClick={() => setPhase("think")}>
              Start — 15s to think
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
