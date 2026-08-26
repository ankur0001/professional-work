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

Walk the intent. Each thread gets its own `SimpleDateFormat` via `withInitial`, avoiding races on a shared mutable formatter. That pattern was common before `java.time`. It still illustrates the mechanics: `get` returns this thread's value, creating it lazily if absent. The danger appears when the thread belongs to a pool and is reused for the next request.

Always `remove` in request-scoped pool usage.

```java
try {
    FMT.get().format(date);
    // or store request context
} finally {
    FMT.remove();
}
```

If you forget `remove`, the value sticks to the worker thread. The next request on that thread may see the previous request's tenant, user, or formatter state. Classic `ThreadLocal` leak: values stick to reused pool threads — remove in `finally`. In long-lived pools, that is not a theoretical concern. It is a security and correctness incident waiting for the unlucky reuse.

Harder reasoning than passing context is the deeper cost. A parameter is visible in the signature. A `ThreadLocal` is invisible ambient state. Callers cannot see what they must set. Tests forget to clear it. New virtual threads multiply instances when you create millions of short-lived threads — each with its own copy — which can amplify memory if values are large or if you accidentally retain them.

Virtual threads make the old "thread pool reuse leak" less universal for some styles, and introduce new pressure: do not treat `ThreadLocal` as free just because threads are cheap. Prefer structured context propagation libraries and explicit parameters for new design. Hold curiosity about structured concurrency; today's warning still stands.

What if we use `ThreadLocal` as a hidden API between layers "so signatures stay clean"?

Signatures stay clean while behavior becomes spooky. A method that only works when someone else set a thread-local upstream is a landmine. If the ambient value is required, at least document and enforce it at a framework boundary — and still remove it on the way out.

Sharing a `ThreadLocal` value across threads somehow — for example by extracting the value and mutating it from another thread — defeats the point and reintroduces races. The isolation is per thread, not "this object is now safe forever."

Request context is the modern form of the problem. Frameworks sometimes offer context objects propagated automatically. That is still ambient state — hopefully with clearer lifecycle. Rolling your own `ThreadLocal` for the same purpose without framework support means you own the enter/exit hooks on every thread that might run your code, including pool workers and callbacks.

SimpleDateFormat in a ThreadLocal was a pre-java.time workaround. Prefer `DateTimeFormatter`, which is immutable and thread-safe, over clever thread confinement for formatting. When a better shared immutable tool exists, take it and delete the ThreadLocal.

Memory leaks with ThreadLocals are not only about correctness of the next request. Large objects retained on idle pool threads pin memory for the life of the pool. `remove` is both a correctness and a footprint discipline.

Inheritable thread locals exist for passing values to child threads — and they surprise people when pools create workers differently than they expect. Prefer explicit propagation. The fewer ambient channels you maintain, the fewer leak hunts you schedule for next quarter.
If you must use ThreadLocal for a request id, set it at the earliest framework filter and remove it at the same layer's exit. Symmetry of enter/exit beats scattered gets in business code.

Picture a legacy library that requires a thread-bound credentials object you cannot change. You set a ThreadLocal in a filter, call the library, and remove in finally. The library is confined; the pool stays clean. That is a justified ThreadLocal. Using the same pattern to avoid adding a parameter to your own new code is not justification — it is avoiding a signature.

Prefer java.time formatters, request parameters, and framework context objects over inventing new ThreadLocals. When you must, pair every `set` or `get`-driven init with a `remove` you can point to in review.

Hold the checklist: prefer parameters; if ThreadLocal is required, set and remove at the same boundary; avoid large retained values on pooled threads; do not hide required context in ambient state for new APIs. Meet those four and ThreadLocal stays a bridge, not a lifestyle.

 When in doubt, pass the context. Ambient state is for the seams you cannot change, not for the code you are writing greenfield this afternoon.

Cleanup is part of the feature, not an afterthought.

So reconnect the chain. Ambient per-thread state solved awkward parameter plumbing and unsafe legacy helpers. `withInitial` made per-thread instances easy. Pool reuse forced `remove` in finally. Hidden APIs and virtual-thread multiplication showed why explicit context is usually healthier. Prefer parameters; use `ThreadLocal` with an exit plan.

When many locks enter a system without a global order, a different failure mode appears — not a leak, but a permanent wait cycle.

Episode Forty-Nine: deadlocks.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 48 (*ThreadLocal*).

Narration technique: ambient-context situation → ThreadLocal → withInitial → remove in pools → hidden API cost → virtual threads foreshadow → next natural problem (deadlocks).
