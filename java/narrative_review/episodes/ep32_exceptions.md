# Episode 32 — Exceptions

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Exceptions |
| Catalog handbook column | 32 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough example |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook`

1. In the last episode, we worked through java.time.
2. If that made sense, today builds on it. If it was fuzzy, today usually makes it click.
3. Exceptions are control flow for failure — design them like an API.
4. I am not going to machine-gun definitions at you.
5. We will go slowly: mental model, worked example, traps, then an interview-ready answer.
6. Settle in for a real lesson — roughly eight to twelve minutes of talking, with room up to about fifteen if you pause on the example.
7. The floor is four minutes, but we are not doing the thin headline version anymore.

### Scene `title`

1. Episode 32.
2. Exceptions.
3. By the end, you should explain this out loud without reading notes.
4. If you can teach it, you own it.

### Scene `concept`

1. First, the why — then the syntax.
2. Picture Exceptions clearly before edge cases.
3. Here are the points that matter when code meets production:
4. Point 1: Checked vs unchecked trade-offs.
5. If you remember only one thing, make it that.
6. Point 2: Don't swallow exceptions.
7. This is usually where tutorials stop — we will not.
8. Point 3: Wrap with context.
9. Point 4: finally vs try-with-resources.
10. Point 5: Create meaningful exception types.
11. That last point is often the senior-level differentiator in interviews.
12. Notice how these points connect: mechanism, usage, and failure mode.
13. Hold them in your head while we look at code.

### Scene `example_intro`

1. Example time. Do not skim.
2. Every line maps to something we just said.
3. If you need to, pause and retype it yourself after the walkthrough.

```java
try {
  read();
} catch (IOException e) {
  throw new UncheckedIOException(e);
}
```

### Scene `example_walk`

1. Walkthrough.
2. I'll walk this like pair-programming.
3. Focus on the idea each line encodes.
4. Then connect to the failure mode.
5. Look at `try {`.
6. That is not decorative syntax — it encodes a real rule of the platform or API.
7. Look at `read();`.
8. Look at `} catch (IOException e) {`.
9. That is not decorative syntax — it encodes a real rule of the platform or API.
10. Look at `throw new UncheckedIOException(e);`.
11. That is not decorative syntax — it encodes a real rule of the platform or API.
12. If you can explain those lines to a teammate, you understand the episode.
13. If you only recognize the keywords, rewind the concept section once.

### Scene `deeper`

1. One level deeper — the part short videos skip.
2. Ask: what happens under load? Under failure? Under bad input?
3. With Exceptions, mastery is not more jargon.
4. Mastery is knowing which trade-off you are choosing: clarity versus speed, flexibility versus safety, simplicity versus control.
5. In production, second-order effects matter: the next engineer’s reading speed, three-a.m. operability, and whether tests still tell the truth.
6. So when you adopt a feature from this episode, adopt the operational story too.
7. Write one sentence in your notes: when I use this, I accept ___, and I mitigate ___ .

### Scene `mistakes`

1. Reality check — common mistakes.
2. Mistake 1: Empty catch blocks.
3. I have seen this in real code reviews — including my own older code.
4. Mistake 2: Using exceptions for ordinary control flow.
5. I have seen this in real code reviews — including my own older code.
6. Mistake 3: Losing the cause chain.
7. I have seen this in real code reviews — including my own older code.
8. If you recognize one, good. Recognition is the first control.

### Scene `interview`

1. Interview time. Speak like someone who has shipped.
2. Question: Checked vs unchecked?
3. Answer: Checked must be declared/handled; unchecked need not — choose intentionally.
4. Then add one trade-off or failure-mode sentence.
5. That extra sentence is what interviewers remember.
6. Practice once without looking at the screen.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Checked vs unchecked trade-offs.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. Don't swallow exceptions.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. Wrap with context.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. finally vs try-with-resources.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. Create meaningful exception types.
19. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
20. If you cannot explain the failure mode, you do not own the feature yet.

### Scene `handbook_spine`

1. How this maps to the reference handbook mindset:
2. The handbook teaches concept, internal working, mistakes, and interview questions.
3. We are doing the same job in spoken form — compressed for video, but not reduced to headlines.
4. So if a section felt familiar, good: that means the curriculum spine is intact.

### Scene `practice`

1. Mini practice before you go.
2. Pause the video and do this without looking:
3. 1) Say out loud what Exceptions is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary`

1. Landing the plane.
2. Today was Exceptions.
3. You got a mental model, a worked example, traps, and an interview answer.
4. Pause and retype the example from memory if you can — that beats passive rewatching.
5. Next time you see this topic in a codebase, you should feel oriented, not lost.

### Scene `teaser`

1. Next episode keeps the story moving.
2. Episode 33: try-with-resources.
3. It builds directly on today’s mental model.
4. If something clicked, stick around. I will see you there.

_Total beats: **100** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **32** — *Exceptions*.
- **Series catalog:** Episode 32 ↔ handbook lesson 32 — *Exceptions*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Programs fail. Networks drop. Files vanish. Users type nonsense._
- **`title`** — starts from: _Episode Thirty-Two._
- **`hierarchy`** — starts from: _Throwable sits at the root of the error hierarchy._
- **`trycatch`** — starts from: _try wraps code that might throw._
- **`throws`** — starts from: _throws declares that a method may propagate an exception._
- **`finally`** — starts from: _finally runs whether the try block succeeds or throws._
- **`custom`** — starts from: _Define custom exceptions when domain errors need clear names._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — checked versus unchecked exceptions?_
- **`teaser`** — starts from: _You know how to catch failure. Next — how to close resources safely._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
