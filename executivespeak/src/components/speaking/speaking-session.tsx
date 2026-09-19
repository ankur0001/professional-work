"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Mic, MicOff, Pause, Square, Volume2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatMinutes } from "@/lib/utils";
import type { FeedbackAnalysis } from "@/lib/schemas/feedback";
import { getTextToSpeechProvider } from "@/lib/providers";

declare global {
  interface Window {
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

interface SpeakingSessionProps {
  scenarioTitle: string;
  initialPrompt: string;
  personality?: string;
  onComplete?: (payload: {
    transcripts: string[];
    analyses: FeedbackAnalysis[];
    durationSeconds: number;
  }) => void;
}

export function SpeakingSession({
  scenarioTitle,
  initialPrompt,
  personality = "executive_coach",
  onComplete,
}: SpeakingSessionProps) {
  const [prompt, setPrompt] = useState(initialPrompt);
  const [transcript, setTranscript] = useState("");
  const [liveLine, setLiveLine] = useState("");
  const [listening, setListening] = useState(false);
  const [paused, setPaused] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [analysis, setAnalysis] = useState<FeedbackAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<{ role: string; text: string }[]>([
    { role: "coach", text: initialPrompt },
  ]);
  const [mustRepeat, setMustRepeat] = useState<string | undefined>();
  const transcriptsRef = useRef<string[]>([]);
  const analysesRef = useRef<FeedbackAnalysis[]>([]);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (paused) return;
    timerRef.current = window.setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current);
    };
  }, [paused]);

  const analyze = useCallback(
    async (text: string, repeatTarget?: string) => {
      setLoading(true);
      try {
        const res = await fetch("/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            transcript: text,
            scenario: scenarioTitle,
            personality,
            mustEvaluateRepeat: repeatTarget,
          }),
        });
        const data = (await res.json()) as FeedbackAnalysis;
        setAnalysis(data);
        analysesRef.current.push(data);
        setHistory((h) => [...h, { role: "coach", text: data.coachMessage }]);
        setMustRepeat(data.mustRepeatPhrase);
        if (data.nextPrompt) {
          setPrompt(data.nextPrompt);
          setHistory((h) => [...h, { role: "coach", text: data.nextPrompt! }]);
        }
      } finally {
        setLoading(false);
      }
    },
    [personality, scenarioTitle],
  );

  const startListening = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setLiveLine("(Microphone STT unavailable — type in the box below and press Submit)");
      return;
    }
    const rec = new SR();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = "en-US";
    rec.onresult = (event: SpeechRecognitionEvent) => {
      let interim = "";
      let final = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const r = event.results[i];
        if (r.isFinal) final += r[0].transcript;
        else interim += r[0].transcript;
      }
      if (final) {
        setTranscript((t) => `${t} ${final}`.trim());
        setLiveLine("");
      } else {
        setLiveLine(interim);
      }
    };
    rec.onerror = () => setListening(false);
    rec.start();
    recognitionRef.current = rec;
    setListening(true);
  }, []);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    recognitionRef.current = null;
    setListening(false);
  }, []);

  const submitSpeech = async () => {
    const text = transcript.trim();
    if (!text) return;
    stopListening();
    setHistory((h) => [...h, { role: "you", text }]);
    transcriptsRef.current.push(text);
    await analyze(text, mustRepeat);
    setTranscript("");
  };

  const endSession = () => {
    stopListening();
    onComplete?.({
      transcripts: transcriptsRef.current,
      analyses: analysesRef.current,
      durationSeconds: seconds,
    });
  };

  const speakCoach = async (text: string) => {
    const tts = getTextToSpeechProvider();
    await tts.speak(text);
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-4 pb-24 lg:p-8">
      <div className="flex items-start justify-between gap-4">
        <div>
          <Badge variant="secondary">{scenarioTitle}</Badge>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">Speaking practice</h1>
          <p className="mt-1 text-sm text-muted-foreground">{prompt}</p>
        </div>
        <div className="text-right text-sm tabular-nums text-muted-foreground">
          {formatMinutes(seconds)}
        </div>
      </div>

      <Card className="border-primary/20 bg-gradient-to-b from-card to-card/50">
        <CardHeader className="items-center pb-2">
          <CardTitle className="text-base font-medium text-muted-foreground">Tap to speak</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center gap-4 pb-8">
          <Button
            size="xl"
            variant={listening ? "destructive" : "default"}
            className="shadow-lg shadow-primary/20"
            onClick={() => (listening ? stopListening() : startListening())}
            disabled={loading || paused}
          >
            {listening ? <MicOff className="h-7 w-7" /> : <Mic className="h-7 w-7" />}
          </Button>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setPaused((p) => !p)}>
              <Pause className="h-4 w-4" /> {paused ? "Resume" : "Pause"}
            </Button>
            <Button variant="outline" size="sm" onClick={endSession}>
              <Square className="h-4 w-4" /> End session
            </Button>
            {analysis?.coachMessage && (
              <Button variant="ghost" size="sm" onClick={() => speakCoach(analysis.coachMessage)}>
                <Volume2 className="h-4 w-4" /> Hear coach
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Live transcript</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="min-h-[80px] rounded-lg bg-muted/40 p-4 text-sm leading-relaxed">
            {transcript || liveLine || (
              <span className="text-muted-foreground">Your words appear here as you speak…</span>
            )}
            {liveLine && transcript && (
              <span className="text-muted-foreground italic"> {liveLine}</span>
            )}
          </div>
          <textarea
            className="w-full rounded-lg border border-input bg-background p-3 text-sm"
            rows={3}
            placeholder="Or type your response if mic is unavailable"
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
          />
          <Button onClick={submitSpeech} disabled={loading || !transcript.trim()} className="w-full">
            {loading ? "Analyzing…" : mustRepeat ? "Submit repeat attempt" : "Submit response"}
          </Button>
        </CardContent>
      </Card>

      {analysis && (
        <Card className="animate-in fade-in slide-in-from-bottom-2">
          <CardHeader>
            <CardTitle className="text-base">Say it better</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <p className="text-muted-foreground">{analysis.coachMessage}</p>
            {analysis.betterPhrases[0] && (
              <div className="grid gap-3 md:grid-cols-3">
                <div className="rounded-lg border p-3">
                  <p className="text-xs font-medium text-muted-foreground">Natural</p>
                  <p className="mt-1">{analysis.betterPhrases[0].natural}</p>
                </div>
                <div className="rounded-lg border p-3">
                  <p className="text-xs font-medium text-muted-foreground">Professional</p>
                  <p className="mt-1">{analysis.betterPhrases[0].professional}</p>
                </div>
                <div className="rounded-lg border border-primary/30 bg-primary/5 p-3">
                  <p className="text-xs font-medium text-primary">Leadership</p>
                  <p className="mt-1">{analysis.betterPhrases[0].leadership}</p>
                </div>
              </div>
            )}
            {analysis.mustRepeatPhrase && (
              <p className="font-medium text-primary">
                Now say the leadership version in your own words.
              </p>
            )}
            {analysis.fillerWords.length > 0 && (
              <p className="text-xs text-muted-foreground">
                Fillers detected:{" "}
                {analysis.fillerWords.map((f) => `${f.word} (${f.count})`).join(", ")}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      <div className="space-y-2">
        {history.map((m, i) => (
          <div
            key={i}
            className={`rounded-lg px-3 py-2 text-sm ${
              m.role === "you" ? "ml-8 bg-primary/10" : "mr-8 bg-muted/50"
            }`}
          >
            <span className="text-xs font-medium uppercase text-muted-foreground">
              {m.role === "you" ? "You" : "Coach"}
            </span>
            <p className="mt-0.5">{m.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
