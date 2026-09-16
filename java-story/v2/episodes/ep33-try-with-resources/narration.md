# Episode 33 — try-with-resources

| Field | Value |
|---|---|
| Episode | 33 |
| Title | try-with-resources |
| Catalog handbook column | 33 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Last time we treated exceptions as part of an API. That conversation almost always collides with another duty: if your code opened something, it must close it.

Picture a method that reads a whole file into memory. You open an input stream, read bytes, and return them. On the happy path you remember to close. On the exception path you might forget. Or you close in `finally`, but `close()` itself throws, and the original read failure disappears behind the close failure. Leaks are not dramatic in a five-minute demo. They are dramatic after a week of open file handles, when the process can no longer open anything new.

So can closing become boring and correct?

Try-with-resources is Java's answer. If a resource implements `AutoCloseable`, you declare it in the try header, and Java closes it when the block exits — whether by return or by exception.

```java
try (var in = Files.newInputStream(path)) {
    return in.readAllBytes();
}
```

`Files.newInputStream(path)` opens the stream. The variable `in` is scoped to the try — it is not floating around the method for someone to misuse after close. When the body finishes, the runtime calls `close()` on `in`. You did not write a `finally`. The structure encodes the rule: if it opens here, it closes here.

Multiple resources belong in one try when their lifetimes match:

```java
try (var in = Files.newInputStream(src);
     var out = Files.newOutputStream(dst)) {
    in.transferTo(out);
}
```

They close in reverse order of declaration — the way you would unwind a stack. Prefer this over manual finally chains that close in the wrong order under stress, or that skip close on an early return you added later.

Suppressed exceptions make the feature trustworthy. Suppose the body throws exception A because the read failed halfway. Then `close()` throws exception B. Older manual patterns often lost A or B depending on how you wrote finally. Try-with-resources keeps A as the primary exception and attaches B as suppressed. Ignoring suppressed exceptions means you only ever see half the story when close fails during an already-failing operation.

Why prefer this over a hand-written finally? Because the hand-written version is easy to almost get right. Null checks, ordering, secondary failures, and early returns all compete for attention while you are also trying to express the business meaning. Try-with-resources removes those degrees of freedom for the common case. Boring is the goal.

Custom resources should follow the same contract. If your class owns a socket, a lock file, or an external session, implement `AutoCloseable` and let callers use try-with-resources:

```java
try (ReportSession session = ReportSession.open(jobId)) {
    return session.render();
}
```

The body focuses on rendering. Cleanup is structural. Once you see resources as values with lifetimes, try-with-resources stops feeling like syntax sugar and starts feeling like the default way to say "this block owns these lifetimes."

Where do people still stumble? Closing only on success. Catching close failures empty-handed. Ignoring suppressed exceptions during incident review. Forgetting resources in tests — tests pass while production leaks, because the test process exits before OS pressure appears.

Notice how this cooperates with the exception story. The primary exception remains the one from your business operation when both body and close fail. That preserves the failure mode operators should chase first, while suppressed exceptions keep the cleanup failure from vanishing. Resource safety and failure forensics are the same design conversation from two angles.

Once closing files is reliable, the next hunger is richer: we want to talk to the filesystem with modern path APIs — create, read, write, walk directories — without living forever in legacy `File` habits.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 33 (*try-with-resources*).

Narration technique: leak/lost-cause situation → try-with-resources → walkthrough → multiple resources → suppressed exceptions → custom AutoCloseable → next natural problem (NIO.2 files).
