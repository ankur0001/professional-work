"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function PronunciationPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Pronunciation</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">architecture</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>Detected issue: stress on second syllable — ar-KI-tec-ture</p>
          <p className="font-mono text-muted-foreground">/ˈɑːrkɪtektʃər/</p>
          <Button size="sm">Repeat</Button>
        </CardContent>
      </Card>
    </div>
  );
}
