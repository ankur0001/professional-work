# Episode 25 — Sorting and Comparators

| Field | Value |
|---|---|
| Episode | 25 |
| Title | Sorting and Comparators |
| Catalog handbook column | 25 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough example |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook`

1. In the last episode, we worked through Queues and Deques.
2. If that made sense, today builds on it. If it was fuzzy, today usually makes it click.
3. Sorting is comparison policy — make that policy explicit and consistent.
4. I am not going to machine-gun definitions at you.
5. We will go slowly: mental model, worked example, traps, then an interview-ready answer.
6. Settle in for a real lesson — roughly eight to twelve minutes of talking, with room up to about fifteen if you pause on the example.
7. The floor is four minutes, but we are not doing the thin headline version anymore.

### Scene `title`

1. Episode 25.
2. Sorting and Comparators.
3. By the end, you should explain this out loud without reading notes.
4. If you can teach it, you own it.

### Scene `concept`

1. First, the why — then the syntax.
2. Picture Sorting and Comparators clearly before edge cases.
3. Here are the points that matter when code meets production:
4. Point 1: Comparable = natural order.
5. If you remember only one thing, make it that.
6. Point 2: Comparator = external strategy.
7. This is usually where tutorials stop — we will not.
8. Point 3: thenComparing chains.
9. Point 4: Consistency with equals matters for sorted sets/maps.
10. Point 5: TimSort is stable for objects.
11. That last point is often the senior-level differentiator in interviews.
12. Notice how these points connect: mechanism, usage, and failure mode.
13. Hold them in your head while we look at code.

### Scene `example_intro`

1. Example time. Do not skim.
2. Every line maps to something we just said.
3. If you need to, pause and retype it yourself after the walkthrough.

```java
list.sort(Comparator.comparing(User::name).thenComparingInt(User::age));
```

### Scene `example_walk`

1. Walkthrough.
2. I'll walk this like pair-programming.
3. Focus on the idea each line encodes.
4. Then connect to the failure mode.
5. Look at `list.sort(Comparator.comparing(User::name).thenComparingInt(User::age));`.
6. If you can explain those lines to a teammate, you understand the episode.
7. If you only recognize the keywords, rewind the concept section once.

### Scene `deeper`

1. One level deeper — the part short videos skip.
2. Ask: what happens under load? Under failure? Under bad input?
3. With Sorting and Comparators, mastery is not more jargon.
4. Mastery is knowing which trade-off you are choosing: clarity versus speed, flexibility versus safety, simplicity versus control.
5. In production, second-order effects matter: the next engineer’s reading speed, three-a.m. operability, and whether tests still tell the truth.
6. So when you adopt a feature from this episode, adopt the operational story too.
7. Write one sentence in your notes: when I use this, I accept ___, and I mitigate ___ .

### Scene `mistakes`

1. Reality check — common mistakes.
2. Mistake 1: Inconsistent compare/equals.
3. I have seen this in real code reviews — including my own older code.
4. Mistake 2: Sorting nulls without nullsFirst/Last.
5. I have seen this in real code reviews — including my own older code.
6. Mistake 3: Mutating objects mid-sort.
7. I have seen this in real code reviews — including my own older code.
8. If you recognize one, good. Recognition is the first control.

### Scene `interview`

1. Interview time. Speak like someone who has shipped.
2. Question: Comparable vs Comparator?
3. Answer: Comparable defines natural order on the type; Comparator is supplied externally.
4. Then add one trade-off or failure-mode sentence.
5. That extra sentence is what interviewers remember.
6. Practice once without looking at the screen.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Comparable = natural order.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. Comparator = external strategy.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. thenComparing chains.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. Consistency with equals matters for sorted sets/maps.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. TimSort is stable for objects.
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
3. 1) Say out loud what Sorting and Comparators is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary`

1. Landing the plane.
2. Today was Sorting and Comparators.
3. You got a mental model, a worked example, traps, and an interview answer.
4. Pause and retype the example from memory if you can — that beats passive rewatching.
5. Next time you see this topic in a codebase, you should feel oriented, not lost.

### Scene `teaser`

1. Next episode keeps the story moving.
2. Episode 26: Streams Intro.
3. It builds directly on today’s mental model.
4. If something clicked, stick around. I will see you there.

_Total beats: **94** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- Series catalog lists this episode under handbook column **25** with title **Sorting and Comparators**.
- Recovered handbook TOC does **not** contain a matching lesson title for this slot (curriculum was remapped for 4–5 minute YouTube pacing).
- Narration was **authored for on-screen visuals** using the episode topic as the outline; concepts reflect standard Java curriculum covered by the handbook’s surrounding lessons, not a verbatim paste.

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
