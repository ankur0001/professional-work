"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { COACH_PERSONALITIES } from "@/lib/data/personalities";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  const [coachPersonality, setCoachPersonality] = useState("executive_coach");
  const [demoMode, setDemoMode] = useState(true);

  useEffect(() => {
    fetch("/api/config").then((r) => r.json()).then((c) => setDemoMode(c.demoMode));
    fetch("/api/profile")
      .then((r) => r.json())
      .then((p) => {
        if (p.coachPersonality) setCoachPersonality(p.coachPersonality);
      });
  }, []);

  async function save() {
    await fetch("/api/profile", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ coachPersonality }),
    });
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Settings</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Coach personality</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Label>Default: Professional Executive Coach</Label>
          <select
            className="w-full rounded-lg border border-input bg-background p-2 text-sm"
            value={coachPersonality}
            onChange={(e) => setCoachPersonality(e.target.value)}
          >
            {COACH_PERSONALITIES.map((p) => (
              <option key={p.id} value={p.id}>
                {p.label}
              </option>
            ))}
          </select>
          <Button onClick={save}>Save</Button>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Privacy</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-muted-foreground">
          <p>Voice: processed for transcription; recordings are not stored unless you enable storage (coming soon).</p>
          <p>Demo mode: {demoMode ? "On" : "Off"}</p>
          <Button variant="outline" size="sm">
            Export data
          </Button>
          <Button variant="destructive" size="sm">
            Delete account
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
