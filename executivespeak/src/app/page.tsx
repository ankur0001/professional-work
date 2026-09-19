import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function HomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-background to-background" />
      <header className="relative mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <div>
          <p className="text-lg font-semibold tracking-tight">ExecutiveSpeak</p>
          <p className="text-xs text-muted-foreground">For software engineers who lead through communication</p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" asChild>
            <Link href="/auth/signin">Sign in</Link>
          </Button>
          <Button asChild>
            <Link href="/auth/signin?demo=1">Try demo</Link>
          </Button>
        </div>
      </header>

      <main className="relative mx-auto max-w-6xl px-6 pb-24 pt-8">
        <Badge className="mb-4">Think → Speak → Improve → Speak again</Badge>
        <h1 className="max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">
          Become a clear, confident, leadership-level communicator.
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-muted-foreground">
          ExecutiveSpeak is not a grammar textbook. It is a premium speaking coach for engineers — meetings,
          technical explanations, presentations, and executive updates — with feedback that makes you speak again.
        </p>
        <div className="mt-10 flex flex-wrap gap-3">
          <Button size="lg" asChild>
            <Link href="/auth/signin?demo=1">Start in demo mode</Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="/auth/signin">Create account</Link>
          </Button>
        </div>

        <section className="mt-20 grid gap-4 md:grid-cols-3">
          {[
            {
              title: "Real workplace scenarios",
              body: "Sprint planning, design disagreements, executive updates, and client conversations.",
            },
            {
              title: "Say it better",
              body: "Natural, professional, and leadership versions — then you speak the stronger phrase aloud.",
            },
            {
              title: "Personal weakness engine",
              body: "Fillers, grammar patterns, and clarity gaps drive tomorrow's practice — not random drills.",
            },
          ].map((f) => (
            <div key={f.title} className="rounded-2xl border border-border/60 bg-card p-6 shadow-sm">
              <h2 className="font-semibold">{f.title}</h2>
              <p className="mt-2 text-sm text-muted-foreground">{f.body}</p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
