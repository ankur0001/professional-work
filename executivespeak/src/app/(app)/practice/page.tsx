import { Suspense } from "react";
import { PracticeClient } from "./practice-client";

export default function PracticePage() {
  return (
    <Suspense fallback={<p className="p-8 text-muted-foreground">Loading practice…</p>}>
      <PracticeClient />
    </Suspense>
  );
}
