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

Picture a method that reads a whole file into memory. You open an input stream, read bytes, and return them. On the happy path you remember to close. On the exception path — a mid-read failure — you might forget. Or you close in `finally`, but `close()` itself throws, and the original read failure disappears behind the close failure. Leaks and lost causes are not dramatic in a demo. They are dramatic after a week of open file handles in production.

So the question writes itself: can closing become boring and correct?

Try-with-resources is Java's answer. If a resource implements `AutoCloseable`, you can declare it in the try header, and Java will close it automatically when the block exits — whether by return or by exception.

```java
try (var in = Files.newInputStream(path)) {
    return in.readAllBytes();
}
```

Walk the mechanics. `Files.newInputStream(path)` opens the stream. The variable `in` is scoped to the try-with-resources. Inside the body you read. When the body finishes, the runtime calls `close()` on `in` for you. You did not write a `finally`. You did not nest close logic beside business logic. The structure itself encodes the rule: if it opens here, it closes here.

Multiple resources belong in one try when their lifetimes match:

```java
try (var in = Files.newInputStream(src);
     var out = Files.newOutputStream(dst)) {
    in.transferTo(out);
}
```

They close in reverse order of declaration. That ordering matches how nested resources usually depend on each other. Prefer this over manual finally chains that close in the wrong order under stress.

Suppressed exceptions are the detail that makes the feature trustworthy. Suppose the body throws exception A, and then `close()` throws exception B. Older manual patterns often lost A or B depending on how you wrote finally. Try-with-resources keeps A as the primary exception and attaches B as a suppressed exception. Debugging tools and logs can surface both. Ignoring suppressed exceptions means you only ever see half the story when close fails during an already-failing operation.

Why prefer this over a hand-written finally close? Because the hand-written version is easy to almost get right. Null checks, ordering, secondary failures, and early returns all compete for attention. Try-with-resources is the pattern that removes those degrees of freedom for the common case.

Custom resources should follow the same contract. If your class owns a socket, a lock file, or an external session, implement `AutoCloseable` (or `Closeable`) and let callers use try-with-resources. That is how your type joins the platform's cleanup story instead of inventing a private `dispose()` ritual everyone forgets.

Where do people still stumble?

Closing in finally incorrectly — closing only on success, or catching close failures empty-handed — recreates the leaks this feature was meant to end. Ignoring suppressed exceptions during incident review hides the close-time clue. Forgetting resources in tests is quieter: tests pass while production leaks, because the test process exits before the OS pressure appears.

So reconnect the chain. Exceptions taught us failure is part of the contract. Open resources taught us success still has duties. Try-with-resources made `AutoCloseable` cleanup automatic, preserved suppressed exceptions, and scaled to multiple resources. Custom types inherit the same discipline.

Once closing files is reliable, the next hunger is richer: we want to talk to the filesystem with modern path APIs — create, read, write, walk directories — without living forever in legacy `File` habits.

That is Episode Thirty-Four: files and NIO.2.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 33 (*try-with-resources*).

Narration technique: leak/lost-cause situation → try-with-resources as answer → walkthrough → multiple resources → suppressed exceptions → custom AutoCloseable → mistakes → next natural problem (NIO.2 files).
