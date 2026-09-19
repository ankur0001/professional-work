"use client";

import { useState } from "react";
import { SpeakingSession } from "@/components/speaking/speaking-session";
import { CONVERSATION_PERSONALITIES } from "@/lib/data/personalities";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ConversationPage() {
  const [personality, setPersonality] = useState("engineering_manager");
  const [started, setStarted] = useState(false);
  const label = CONVERSATION_PERSONALITIES.find((p) => p.id === personality)?.label ?? "Coach";

  if (!started) {
    return (
      <div className="mx-auto max-w-2xl space-y-6 p-8">
        <h1 className="text-3xl font-semibold">AI conversation mode</h1>
        <p className="text-muted-foreground">
          Choose a personality. The AI lets you finish speaking, then continues naturally with coaching feedback.
        </p>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Personality</CardTitle>
          </CardHeader>
          <CardContent>
            <select
              className="w-full rounded-lg border border-input bg-background p-2 text-sm"
              value={personality}
              onChange={(e) => setPersonality(e.target.value)}
            >
              {CONVERSATION_PERSONALITIES.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.label} — {p.description}
                </option>
              ))}
            </select>
            <button
              type="button"
              className="mt-4 w-full rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground"
              onClick={() => setStarted(true)}
            >
              Start conversation
            </button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <SpeakingSession
      scenarioTitle={`Conversation · ${label}`}
      initialPrompt="You're presenting a proposal to your manager. Explain why you want to migrate the service to a new architecture."
      personality={personality}
    />
  );
}
