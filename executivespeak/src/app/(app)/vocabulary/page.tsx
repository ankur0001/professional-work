"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function VocabularyPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Vocabulary engine</h1>
      <p className="text-muted-foreground">
        Words are learned from your real speech patterns with spaced repetition (Phase 2 expands tracking).
      </p>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Suggested upgrades</CardTitle>
        </CardHeader>
        <CardContent className="text-sm">
          <p>Instead of &quot;good&quot; → effective, reliable, scalable</p>
          <p className="mt-2">Instead of &quot;problem&quot; → issue, risk, bottleneck, trade-off</p>
        </CardContent>
      </Card>
    </div>
  );
}
