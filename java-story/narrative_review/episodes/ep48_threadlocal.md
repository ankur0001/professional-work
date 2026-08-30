# Episode 48 — ThreadLocal

| Field | Value |
|---|---|
| Episode | 48 |
| Title | ThreadLocal |
| Catalog handbook column | 48 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Fork/Join and pools make threads into shared workers. That sharing collides with an older convenience: sometimes people stash data "on the thread" so deep call stacks need not pass it as a parameter. A request id for logging. A tenant id. A non-thread-safe formatter reused without locking. The convenience is real. So is the leak.

`ThreadLocal` is per-thread global state — powerful and leak-prone. Prefer explicit context parameters when possible. Use `ThreadLocal` when interoperation with legacy APIs or cross-cutting instrumentation truly needs ambient state — and then treat cleanup as part of the design.

```java
static final ThreadLocal<SimpleDateFormat> FMT =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));
```

Each thread gets its own `SimpleDateFormat` via `withInitial`, avoiding races on a shared mutable formatter. That pattern was common before `java.time`. It still illustrates the mechanics: `get` returns this thread's value, creating it lazily if absent. The danger appears when the thread belongs to a pool and is reused for the next request.

Always `remove` in request-scoped pool usage:

```java
try {
    FMT.get().format(date);
} finally {
    FMT.remove();
}
```

If you forget `remove`, the value sticks to the worker thread. The next request on that thread may see the previous request's tenant, user, or formatter state. Classic `ThreadLocal` leak: values stick to reused pool threads. In long-lived pools, that is a security and correctness incident waiting for the unlucky reuse.

Harder reasoning than passing context is the deeper cost. A parameter is visible in the signature. A `ThreadLocal` is invisible ambient state. Callers cannot see what they must set. Tests forget to clear it. New virtual threads multiply instances when you create millions of short-lived threads — each with its own copy — which can amplify memory if values are large.

What if we use `ThreadLocal` as a hidden API between layers "so signatures stay clean"? Signatures stay clean while behavior becomes spooky. A method that only works when someone else set a thread-local upstream is a landmine. If the ambient value is required, at least document and enforce it at a framework boundary — and still remove it on the way out.

`SimpleDateFormat` in a ThreadLocal was a pre-java.time workaround. Prefer `DateTimeFormatter`, which is immutable and thread-safe, over clever thread confinement for formatting. When a better shared immutable tool exists, take it and delete the ThreadLocal.

Memory leaks with ThreadLocals are not only about correctness of the next request. Large objects retained on idle pool threads pin memory for the life of the pool. `remove` is both a correctness and a footprint discipline.

If you must use ThreadLocal for a request id, set it at the earliest framework filter and remove it at the same layer's exit. Symmetry of enter/exit beats scattered gets in business code.

Picture a legacy library that requires a thread-bound credentials object you cannot change. You set a ThreadLocal in a filter, call the library, and remove in finally. The library is confined; the pool stays clean. That is a justified ThreadLocal. Using the same pattern to avoid adding a parameter to your own new code is not justification — it is avoiding a signature.

Hold the checklist: prefer parameters; if ThreadLocal is required, set and remove at the same boundary; avoid large retained values on pooled threads; do not hide required context in ambient state for new APIs. When in doubt, pass the context. Ambient state is for the seams you cannot change, not for greenfield code this afternoon.

When many locks enter a system without a global order, a different failure mode appears — not a leak, but a permanent wait cycle.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 48 (*ThreadLocal*).

Narration technique: ambient-context situation → ThreadLocal → withInitial → remove in pools → hidden API cost → next natural problem (deadlocks).
