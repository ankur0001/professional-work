import { PHRASE_LIBRARY } from "@/lib/data/phrases";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function PhrasebookPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-8">
      <h1 className="text-3xl font-semibold">Professional phrase library</h1>
      {PHRASE_LIBRARY.map((cat) => (
        <Card key={cat.category}>
          <CardHeader>
            <CardTitle className="text-base">{cat.category}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            {cat.phrases.map((p) => (
              <p key={p} className="rounded-lg bg-muted/40 px-3 py-2">
                {p}
              </p>
            ))}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
