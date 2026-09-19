"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getTextToSpeechProvider } from "@/lib/providers";

interface PronEntry {
  word: string;
  issue: string;
  ipa: string;
  slowTip: string;
}

export default function PronunciationPage() {
  const [focus, setFocus] = useState<PronEntry[]>([]);
  const [bank, setBank] = useState<PronEntry[]>([]);

  useEffect(() => {
    fetch("/api/pronunciation")
      .then((r) => r.json())
      .then((d) => {
        setFocus(d.focus ?? []);
        setBank(d.bank ?? []);
      });
  }, []);

  async function speak(word: string, rate = 1) {
    const tts = getTextToSpeechProvider();
    await tts.speak(word, { rate });
  }

  const list = focus.length ? focus : bank.slice(0, 3);

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Pronunciation</h1>
      <p className="text-muted-foreground">
        Words detected from your sessions appear here. Practice stress and clarity — not &quot;wrong pronunciation&quot;
        shaming.
      </p>
      {list.map((entry) => (
        <Card key={entry.word}>
          <CardHeader>
            <CardTitle className="text-base">{entry.word}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <p>{entry.issue}</p>
            <p className="font-mono text-muted-foreground">{entry.ipa}</p>
            <p className="text-xs text-muted-foreground">Slow: {entry.slowTip}</p>
            <div className="flex gap-2 pt-2">
              <Button size="sm" variant="outline" onClick={() => speak(entry.word, 0.85)}>
                Slow
              </Button>
              <Button size="sm" onClick={() => speak(entry.word, 1)}>
                Normal
              </Button>
              <Button size="sm" variant="secondary">
                Repeat aloud
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
