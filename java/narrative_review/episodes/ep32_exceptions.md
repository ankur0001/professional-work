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

Suppose your service must load a configuration file at startup. The happy path reads bytes, parses settings, and continues. The unhappy path is just as real: the file is missing, the disk is full, permissions deny access. If you pretend failure is rare enough to ignore, you do not get a cleaner program — you get a crash with no context, or worse, a silent wrong default that looks healthy until noon traffic arrives.

So a natural question appears: how should a method announce that it could not do its job?

That is what exceptions are for. They are control flow for failure. Treat them like part of the API, not like an embarrassing side channel you only mention in comments.

Java splits the space into checked and unchecked exceptions, and the split is a design choice, not trivia. Checked exceptions must be declared or handled. They push the caller to acknowledge a failure mode the type system can see — classic I/O and certain library operations live here. Unchecked exceptions — subclasses of `RuntimeException` — need not be declared. They often represent programming mistakes or failures you do not expect every caller to recover from locally. Neither family is "always better." The question is whether the failure is part of the method's honest contract with its callers.

Here is a small illustration of wrapping with context instead of leaking a low-level type through every layer:

```java
try {
    read();
} catch (IOException e) {
    throw new UncheckedIOException("failed reading config " + path, e);
}
```

Walk it. `read()` can fail with `IOException`. Catching it and throwing `UncheckedIOException` with a message and `e` as the cause preserves the original failure while changing how callers are forced to react. The cause chain matters. If you catch and throw a new exception without attaching the cause, you erase the forensic trail that production debugging needs. Months later, someone will see "something failed" and have no idea that the root was a permission error on a specific path.

That example also hints at a discipline: do not swallow exceptions.

```java
try {
    read();
} catch (IOException e) {
    // empty — the bug that teaches nothing
}
```

An empty catch block makes the program continue as if success happened. The failure is still there; you only removed the evidence. If you catch, either recover meaningfully, translate with context, or rethrow. Logging and continuing can be valid — but only when that is an intentional policy, not a reflex to silence the compiler.

`finally` exists for cleanup that must run whether the try block succeeded or threw. You will still see it in older code:

```java
InputStream in = open();
try {
    return in.readAllBytes();
} finally {
    if (in != null) {
        in.close();
    }
}
```

This pattern is easy to almost get right and hard to get perfect when `close()` itself throws. Modern Java prefers try-with-resources when the thing you opened implements `AutoCloseable` — and that story deserves its own episode, because the close path has subtle failure modes of its own. For today, hold the rule lightly: if the point of the block is "close this resource," there is a better tool coming next.

Meaningful exception types are the other half of API design. A generic `RuntimeException("failed")` tells the caller almost nothing. A domain exception — `OrderNotFoundException`, `InvalidTaxRateException` — lets upper layers choose policy: retry, skip, surface to the user, page an operator. Create types when the failure mode is part of your vocabulary, not when you merely want a different name for "something went wrong."

What if we use exceptions for ordinary control flow — for example, throwing to mean "not found" on a hot path that is usually empty?

It can work mechanically and still be the wrong shape. Exceptions are expensive compared with a normal branch, and they obscure the expected path. Prefer return values, `Optional`, or explicit result types for common, non-exceptional outcomes. Reserve throws for genuine failure or truly exceptional conditions your API wants to force upward.

Think about the call stack for a moment. A low-level I/O helper throws `IOException`. A repository catches it and throws `ConfigLoadException` with the path and the cause. A startup component catches that and decides whether to abort the process or fall back to defaults. Each layer adds the decision it is qualified to make. That is what "design exceptions like an API" means in practice — not inventing twenty subclasses for fun, but placing failure information where policy can use it.

If every method only logs and returns null on failure, you have not removed exceptions. You have replaced them with a quieter protocol that callers must remember to check, and that the compiler will not help enforce. Sometimes that quieter protocol is `Optional` or a result type — and that can be right for expected absence. For true operational failure, an exception that preserves context is often the clearer contract.

So reconnect the chain. We started with a missing config file and asked how failure should travel. Exceptions answered as failure-shaped control flow. Checked versus unchecked became an intentional contract choice. Wrapping preserved context. Swallowing and cause-loss showed the forensic failures. Domain types made failures speak the language of the product. Misusing throws as a fancy `goto` showed the boundary with ordinary control flow.

Once you accept that resources must open and may fail, a sharper problem appears: even on the success path, an open file, socket, or stream must be closed. Doing that correctly in every `finally` is tedious — and easy to get slightly wrong when close itself throws.

That is exactly why Episode Thirty-Three exists: try-with-resources.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 32 (*Exceptions*).

Narration technique: failed I/O situation → exceptions as failure API → checked/unchecked → wrap with cause → swallow anti-pattern → finally foreshadow → domain types → misuse → next natural problem (try-with-resources).
