"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { getDailyPlan } from "@/lib/data/scenarios";
import { greetingForHour } from "@/lib/utils";
import { ACHIEVEMENT_CATALOG } from "@/lib/data/achievements";

interface Profile {
  name?: string;
  dailyPracticeMinutes?: number;
  currentLevelLabel?: string;
  communicationScores?: Record<string, number>;
  totalSpeakingMinutes?: number;
  streakDays?: number;
  achievements?: string[];
}

interface DailyChallenge {
  id: string;
  title: string;
  prompt: string;
}

export default function DashboardPage() {
  const [profile, setProfile] = useState<Profile>({});
  const [demoMode, setDemoMode] = useState(true);
  const [challenge, setChallenge] = useState<DailyChallenge | null>(null);
  const [challengeDone, setChallengeDone] = useState(false);
  const [curriculum, setCurriculum] = useState<{
    focus: string;
    minutes: number;
    weaknessTargets: string[];
    items: { title: string; prompt: string; slug: string }[];
  } | null>(null);
  const plan = getDailyPlan(profile.dailyPracticeMinutes ?? 20);
  const focusText = curriculum?.focus ?? plan.focus;
  const practiceMinutes = curriculum?.minutes ?? plan.minutes;
  const spokenToday = 0;
  const progressPct = Math.min(100, (spokenToday / practiceMinutes) * 100);

  useEffect(() => {
    fetch("/api/config").then((r) => r.json()).then((c) => setDemoMode(c.demoMode));
    fetch("/api/profile")
      .then((r) => r.json())
      .then(setProfile)
      .catch(() => undefined);
    fetch("/api/challenges/daily")
      .then((r) => r.json())
      .then((d) => {
        setChallenge(d.challenge);
        setChallengeDone(d.completed);
      })
      .catch(() => undefined);
    fetch("/api/curriculum/today")
      .then((r) => r.json())
      .then(setCurriculum)
      .catch(() => undefined);
  }, []);

  const scores = profile.communicationScores ?? {};

  return (
    <div className="mx-auto max-w-6xl space-y-8 p-6 lg:p-10">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-muted-foreground">{greetingForHour()}{profile.name ? `, ${profile.name}` : ""}.</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Today&apos;s practice</h1>
          {demoMode && <Badge variant="outline" className="mt-2">Demo mode — mock AI & optional database</Badge>}
        </div>
        <div className="text-right text-sm text-muted-foreground">
          Streak: {profile.streakDays ?? 0} days · {profile.totalSpeakingMinutes ?? 0} min spoken total
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">Today&apos;s goal</CardTitle>
            <CardDescription>{plan.minutes} minutes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <div
                className="relative h-20 w-20 rounded-full border-4 border-primary/20"
                style={{
                  background: `conic-gradient(var(--primary) ${progressPct * 3.6}deg, var(--muted) 0)`,
                }}
              />
              <div>
                <p className="text-2xl font-semibold">{Math.round(progressPct)}%</p>
                <p className="text-xs text-muted-foreground">Progress ring</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">Current level</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-xl font-semibold">{profile.currentLevelLabel ?? "Professional Communicator"}</p>
            <p className="mt-2 text-sm text-muted-foreground">Based on demonstrated performance in sessions.</p>
          </CardContent>
        </Card>

        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">Today&apos;s focus</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">{focusText}</p>
            {curriculum?.weaknessTargets?.length ? (
              <ul className="mt-2 list-disc pl-5 text-xs text-muted-foreground">
                {curriculum.weaknessTargets.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            ) : null}
            <p className="mt-3 text-sm font-medium">Challenge</p>
            <p className="text-sm text-muted-foreground">{plan.challenge}</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Communication dimensions</CardTitle>
          <CardDescription>Coaching metrics from your baseline and recent sessions</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {[
            ["Fluency", scores.speakingFluency ?? scores.fluency],
            ["Grammar", scores.grammar],
            ["Vocabulary", scores.vocabulary],
            ["Pronunciation", scores.pronunciation],
            ["Clarity", scores.clarity],
            ["Confidence", scores.confidence],
            ["Conciseness", scores.conciseness],
            ["Leadership", scores.leadershipCommunication ?? scores.leadership],
            ["Technical", scores.technicalExplanation],
            ["Storytelling", scores.storytelling ?? scores.naturalness],
          ].map(([label, val]) => (
            <div key={label as string}>
              <div className="mb-1 flex justify-between text-xs">
                <span>{label}</span>
                <span className="tabular-nums">{val ?? "—"}</span>
              </div>
              <Progress value={Number(val) || 0} />
            </div>
          ))}
        </CardContent>
      </Card>

      {challenge && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Daily leadership challenge</CardTitle>
            <CardDescription>{challengeDone ? "Completed today" : challenge.title}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <p>{challenge.prompt}</p>
            <Button asChild variant={challengeDone ? "secondary" : "default"}>
              <Link href={`/practice?scenario=leadership-design-disagreement`}>
                {challengeDone ? "Practice again" : "Start challenge"}
              </Link>
            </Button>
          </CardContent>
        </Card>
      )}

      {(profile.achievements?.length ?? 0) > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Achievements</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {profile.achievements!.map((slug) => (
              <Badge key={slug} variant="outline">
                {ACHIEVEMENT_CATALOG[slug]?.title ?? slug}
              </Badge>
            ))}
          </CardContent>
        </Card>
      )}

      <Card className="border-primary/20 bg-gradient-to-br from-card to-primary/5">
        <CardHeader>
          <CardTitle>Today&apos;s practice</CardTitle>
          <CardDescription>🔥 ~{plan.minutes} minute speaking session</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm">
            <span className="font-medium">Scenario:</span>{" "}
            {plan.items.find((i) => i.type === "leadership")?.prompt ??
              "You are leading a sprint planning meeting."}
          </p>
          <div className="flex flex-wrap gap-2">
            <Button asChild size="lg">
              <Link href="/practice?mode=standard">Start practice</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/practice?mode=quick">Quick practice</Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/practice?mode=deep">Deep practice</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
