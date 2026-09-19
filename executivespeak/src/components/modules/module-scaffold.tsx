import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function ModuleScaffold({
  title,
  description,
  scenarios,
}: {
  title: string;
  description: string;
  scenarios: { slug: string; title: string; prompt: string }[];
}) {
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 lg:p-10">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">{description}</p>
      </div>
      <div className="grid gap-4">
        {scenarios.map((s) => (
          <Card key={s.slug}>
            <CardHeader>
              <CardTitle className="text-base">{s.title}</CardTitle>
              <CardDescription>{s.prompt}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild>
                <Link href={`/practice?scenario=${s.slug}`}>Start speaking</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
