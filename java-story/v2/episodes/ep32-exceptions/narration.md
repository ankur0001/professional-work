# Episode 32 — Exceptions

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Exceptions |
| Catalog handbook column | 32 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Time became a typed contract. That helps when values are valid. It does not help when the world refuses to cooperate.

Suppose your service must load a configuration file at startup. The happy path reads, parses, and continues. The unhappy path is just as real: the file is missing, the disk is full, permissions deny access. Ignore failure and you get a crash with no context — or a silent wrong default that looks healthy until noon traffic arrives.

So how should a method announce that it could not do its job?

Exceptions are control flow for failure. Treat them as part of the API, not an embarrassing side channel mentioned only in comments.

Java splits checked and unchecked exceptions, and the split is a design choice. Checked exceptions must be declared or handled — they push the caller to acknowledge a failure mode the type system can see. Unchecked exceptions — subclasses of `RuntimeException` — need not be declared; they often represent programming mistakes or failures you do not expect every caller to recover from locally. Neither family is always better. The question is whether the failure is part of the method's honest contract.

Here is wrapping with context instead of leaking a low-level type through every layer:

```java
try {
    read();
} catch (IOException e) {
    throw new UncheckedIOException("failed reading config " + path, e);
}
```

`read()` can fail with `IOException`. Catching and throwing `UncheckedIOException` with a message and `e` as the cause preserves the original failure while changing how callers must react. The cause chain matters. Catch and throw a new exception without the cause, and you erase the forensic trail production debugging needs.

Do not swallow exceptions:

```java
try {
    read();
} catch (IOException e) {
    // empty — the bug that teaches nothing
}
```

An empty catch makes the program continue as if success happened. If you catch, either recover meaningfully, translate with context, or rethrow. Logging and continuing can be valid — only as intentional policy, not as a reflex to silence the compiler.

`finally` exists for cleanup that must run whether the try succeeded or threw. You will still see it in older code:

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

This pattern is easy to almost get right and hard to get perfect when `close()` itself throws. Modern Java prefers try-with-resources when the thing you opened implements `AutoCloseable` — and that story deserves its own space, because the close path has subtle failure modes. Hold the rule lightly: if the point of the block is "close this resource," a better tool is coming.

Meaningful exception types are the other half of API design. A generic `RuntimeException("failed")` tells the caller almost nothing. A domain exception — `OrderNotFoundException`, `InvalidTaxRateException` — lets upper layers choose policy: retry, skip, surface to the user, page an operator. Create types when the failure mode is part of your vocabulary.

What if we use exceptions for ordinary control flow — throwing to mean "not found" on a hot path that is usually empty? It can work mechanically and still be the wrong shape. Exceptions are expensive compared with a normal branch, and they obscure the expected path. Prefer return values, `Optional`, or explicit result types for common, non-exceptional outcomes. Reserve throws for genuine failure.

Think about the call stack. A low-level I/O helper throws `IOException`. A repository catches it and throws `ConfigLoadException` with the path and the cause. A startup component decides whether to abort or fall back. Each layer adds the decision it is qualified to make. That is what "design exceptions like an API" means — not inventing twenty subclasses for fun, but placing failure information where policy can use it.

If every method only logs and returns null on failure, you have not removed exceptions. You have replaced them with a quieter protocol callers must remember to check. Sometimes that quieter protocol is `Optional` — right for expected absence. For true operational failure, an exception that preserves context is often the clearer contract.

Once you accept that resources must open and may fail, a sharper problem appears: even on the success path, an open file, socket, or stream must be closed. Doing that correctly in every `finally` is tedious — and easy to get slightly wrong when close itself throws.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 32 (*Exceptions*).

Narration technique: failed I/O situation → exceptions as failure API → checked/unchecked → wrap with cause → swallow anti-pattern → finally foreshadow → domain types → next natural problem (try-with-resources).
