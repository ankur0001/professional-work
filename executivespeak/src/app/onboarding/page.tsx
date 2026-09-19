"use client";

import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const STEPS = 10;

export default function OnboardingPage() {
  const { status } = useSession();
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    name: "",
    profession: "Software Engineer",
    yearsExperience: 5,
    englishLevel: "intermediate",
    communicationProblems: [] as string[],
    nativeLanguage: "",
    targetAccent: "american",
    dailyPracticeMinutes: 20,
    primaryGoal: "leadership",
    confidenceScore: 6,
  });

  useEffect(() => {
    if (status === "unauthenticated") router.replace("/auth/signin");
  }, [status, router]);

  useEffect(() => {
    fetch("/api/profile")
      .then((r) => r.json())
      .then((p) => {
        if (p?.onboardingCompleted) router.replace("/dashboard");
        if (p?.name) setForm((f) => ({ ...f, name: p.name }));
      })
      .catch(() => undefined);
  }, [router]);

  const toggleProblem = (p: string) => {
    setForm((f) => ({
      ...f,
      communicationProblems: f.communicationProblems.includes(p)
        ? f.communicationProblems.filter((x) => x !== p)
        : [...f.communicationProblems, p],
    }));
  };

  async function finishOnboarding() {
    await fetch("/api/profile", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, onboardingCompleted: false }),
    });
    router.push("/onboarding/baseline");
  }

  const progress = ((step + 1) / STEPS) * 100;

  return (
    <div className="mx-auto min-h-screen max-w-xl px-4 py-10">
      <p className="text-sm font-medium text-primary">ExecutiveSpeak onboarding</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">Build your coaching profile</h1>
      <Progress value={progress} className="mt-6" />

      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Step {step + 1} of {STEPS}</CardTitle>
          <CardDescription>This baseline helps personalize scenarios — not a standardized test score.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {step === 0 && (
            <div className="space-y-2">
              <Label>Your name</Label>
              <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
          )}
          {step === 1 && (
            <div className="space-y-2">
              <Label>Current profession</Label>
              <Input
                value={form.profession}
                onChange={(e) => setForm({ ...form, profession: e.target.value })}
              />
            </div>
          )}
          {step === 2 && (
            <div className="space-y-2">
              <Label>Years of experience</Label>
              <Input
                type="number"
                value={form.yearsExperience}
                onChange={(e) => setForm({ ...form, yearsExperience: Number(e.target.value) })}
              />
            </div>
          )}
          {step === 3 && (
            <div className="space-y-2">
              <Label>Current English level</Label>
              <select
                className="w-full rounded-lg border border-input bg-background p-2 text-sm"
                value={form.englishLevel}
                onChange={(e) => setForm({ ...form, englishLevel: e.target.value })}
              >
                <option value="basic">Basic</option>
                <option value="intermediate">Intermediate</option>
                <option value="upper-intermediate">Upper intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          )}
          {step === 4 && (
            <div className="space-y-2">
              <Label>Main communication problems</Label>
              <div className="flex flex-wrap gap-2">
                {["fillers", "hesitation", "grammar", "vocabulary", "pronunciation", "clarity", "confidence"].map(
                  (p) => (
                    <Button
                      key={p}
                      type="button"
                      size="sm"
                      variant={form.communicationProblems.includes(p) ? "default" : "outline"}
                      onClick={() => toggleProblem(p)}
                    >
                      {p}
                    </Button>
                  ),
                )}
              </div>
            </div>
          )}
          {step === 5 && (
            <div className="space-y-2">
              <Label>Native language</Label>
              <Input
                value={form.nativeLanguage}
                onChange={(e) => setForm({ ...form, nativeLanguage: e.target.value })}
              />
            </div>
          )}
          {step === 6 && (
            <div className="space-y-2">
              <Label>Target accent</Label>
              <select
                className="w-full rounded-lg border border-input bg-background p-2 text-sm"
                value={form.targetAccent}
                onChange={(e) => setForm({ ...form, targetAccent: e.target.value })}
              >
                <option value="american">American</option>
                <option value="british">British</option>
                <option value="neutral">Neutral international English</option>
              </select>
            </div>
          )}
          {step === 7 && (
            <div className="space-y-2">
              <Label>Daily practice time</Label>
              <select
                className="w-full rounded-lg border border-input bg-background p-2 text-sm"
                value={form.dailyPracticeMinutes}
                onChange={(e) => setForm({ ...form, dailyPracticeMinutes: Number(e.target.value) })}
              >
                {[10, 20, 30, 45, 60].map((m) => (
                  <option key={m} value={m}>
                    {m} minutes
                  </option>
                ))}
              </select>
            </div>
          )}
          {step === 8 && (
            <div className="space-y-2">
              <Label>Primary goal</Label>
              <select
                className="w-full rounded-lg border border-input bg-background p-2 text-sm"
                value={form.primaryGoal}
                onChange={(e) => setForm({ ...form, primaryGoal: e.target.value })}
              >
                <option value="workplace">Workplace communication</option>
                <option value="leadership">Leadership</option>
                <option value="interviews">Interviews</option>
                <option value="presentations">Presentations</option>
                <option value="client">Client communication</option>
                <option value="management">Management</option>
                <option value="fluency">General fluency</option>
              </select>
            </div>
          )}
          {step === 9 && (
            <div className="space-y-2">
              <Label>Confidence speaking English (1–10): {form.confidenceScore}</Label>
              <input
                type="range"
                min={1}
                max={10}
                value={form.confidenceScore}
                onChange={(e) => setForm({ ...form, confidenceScore: Number(e.target.value) })}
                className="w-full"
              />
            </div>
          )}

          <div className="flex justify-between pt-4">
            <Button type="button" variant="outline" disabled={step === 0} onClick={() => setStep((s) => s - 1)}>
              Back
            </Button>
            {step < STEPS - 1 ? (
              <Button type="button" onClick={() => setStep((s) => s + 1)}>
                Continue
              </Button>
            ) : (
              <Button type="button" onClick={finishOnboarding}>
                Start baseline speaking assessment
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
