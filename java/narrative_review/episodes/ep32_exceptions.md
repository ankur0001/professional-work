# Episode 32 — Exceptions

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Exceptions |
| Catalog handbook column | 32 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

In the last episode, time became a typed contract. That helps when values are valid. It does not help when the world refuses to cooperate.

Suppose your service must load a configuration file at startup. The happy path reads bytes and continues. The unhappy path is just as real: the file is missing, the disk is full, permissions deny access. If you pretend failure is rare enough to ignore, you do not get a cleaner program — you get a crash with no context, or worse, a silent wrong default.

So a natural question appears: how should a method announce that it could not do its job?

That is what exceptions are for. They are control flow for failure. Treat them like part of the API, not like an embarrassing side channel.

Java splits the space into checked and unchecked exceptions, and the split is a design choice, not trivia. Checked exceptions must be declared or handled. They push the caller to acknowledge a failure mode the type system can see — classic I/O and certain library operations live here. Unchecked exceptions — subclasses of `RuntimeException` — need not be declared. They often represent programming mistakes or failures you do not expect every caller to recover from locally. Neither family is "always better." The question is whether the failure is part of the method's honest contract.

Here is a small illustration of wrapping with context instead of leaking a low-level type through every layer:

```java
try {
    read();
} catch (IOException e) {
    throw new UncheckedIOException(e);
}
```

Walk it. `read()` can fail with `IOException`. Catching it and throwing `UncheckedIOException` with `e` as the cause preserves the original failure while changing how callers are forced to react. The cause chain matters. If you catch and throw a new exception without attaching the cause, you erase the forensic trail that production debugging needs.

That example also hints at a discipline: do not swallow exceptions.

```java
try {
    read();
} catch (IOException e) {
    // empty — the bug that teaches nothing
}
```

An empty catch block makes the program continue as if success happened. The failure is still there; you only removed the evidence. If you catch, either recover meaningfully, translate with context, or rethrow. Logging and continuing can be valid — but only when that is an intentional policy, not a reflex to silence the compiler.

`finally` exists for cleanup that must run whether the try block succeeded or threw. You will still see it in older code. Modern Java prefers try-with-resources when the thing you opened implements `AutoCloseable` — and that story deserves its own episode, because the close path has subtle failure modes of its own. For today, hold the rule lightly: if the point of the block is "close this resource," there is a better tool coming.

Meaningful exception types are the other half of API design. A generic `RuntimeException("failed")` tells the caller almost nothing. A domain exception — `OrderNotFoundException`, `InvalidTaxRateException` — lets upper layers choose policy: retry, skip, surface to the user, page an operator. Create types when the failure mode is part of your vocabulary, not when you merely want a different name for "something went wrong."

What if we use exceptions for ordinary control flow — for example, throwing to mean "not found" on a hot path that is usually empty?

It can work mechanically and still be the wrong shape. Exceptions are expensive compared with a normal branch, and they obscure the expected path. Prefer return values, `Optional`, or explicit result types for common, non-exceptional outcomes. Reserve throws for genuine failure or truly exceptional conditions your API wants to force upward.

So reconnect the chain. We started with a missing config file and asked how failure should travel. Exceptions answered as failure-shaped control flow. Checked versus unchecked became an intentional contract choice. Wrapping preserved context. Swallowing and cause-loss showed the forensic failures. Domain types made failures speak the language of the product.

Once you accept that resources must open and may fail, a sharper problem appears: even on the success path, an open file, socket, or stream must be closed. Doing that correctly in every `finally` is tedious — and easy to get slightly wrong when close itself throws.

That is exactly why Episode Thirty-Three exists: try-with-resources.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 32 (*Exceptions*).

Narration technique: failed I/O situation → exceptions as failure API → checked/unchecked → wrap with cause → swallow anti-pattern → finally foreshadow → domain types → misuse → next natural problem (try-with-resources).
