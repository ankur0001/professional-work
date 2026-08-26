# Episode 65 — JVM Startup

| Field | Value |
|---|---|
| Episode | 65 |
| Title | JVM Startup |
| Catalog handbook column | 65 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Steady-state performance has dominated our recent episodes: GC, JIT warmup, safepoints, heap shape. Then you deploy to a scale-to-zero environment, or you restart pods on every deploy, or you run short-lived CLI tools that should feel instant. Suddenly the question is not p99 after warmup. The question is how long from process start until the app can do useful work. Startup is a feature. Teams that only optimize the warmed steady state discover that truth the first time readiness probes fail in a rolling deploy.

```bash
java -jar app.jar
# measure cold start separately from steady-state
```

That command looks simple. Behind it, the JVM loads classes, verifies bytecode, initializes classes, runs static initializers, and begins with a cold JIT. Your framework likely scans the classpath, wires beans, opens connection pools, and warms caches you did not ask to warm at boot. Classloading, verification, and initialization dominate many cold starts. A fat classpath makes that worse — every jar is more work before business logic matters. Ignoring classpath bloat while "optimizing startup" is rearranging furniture during a flood.

Heavy work in static initializers is a classic self-inflicted wound. A class loads because something touched it, its static initializer hits a database or builds a giant cache, and first-request latency includes an accidental boot ritual. Lazy initialization helps — carefully. Lazy means "not at class init time," not "no concurrency story." Initialize on first use with clear thread safety, or on a deliberate lifecycle hook you can see in metrics and logs.

Distinguish three clocks teams mix up. Wall time to process start is not wall time to readiness, which is not wall time to stable p99 after JIT warmup. A service can pass a shallow readiness probe while still loading classes lazily on the first real traffic wave. Another can be "slow to start" because static initializers do work that should be a deliberate warm step with metrics. Measure each clock separately or you optimize the wrong one.

The platform offers acceleration once you understand the cost drivers. CDS and AppCDS archive class metadata so subsequent runs spend less time loading and linking common classes. Ahead-of-time compilation and Graal native image trade some dynamic JIT flexibility and reflection freedom for a native binary with faster startup and a different peak-performance profile. CRaC — Coordinated Restore at Checkpoint — aims at snapshotted restarts: warm a process, checkpoint, restore later into a ready state. Each technique has a fit. None is free. Native image constraints surprise teams that relied on runtime reflection everywhere. Checkpoint restore needs discipline about what state is safe to freeze.

Classpath bloat has a human story. Someone adds a starter for one annotation processor, transitive jars multiply, boot scanning grows. Native image later looks attractive because startup hurt — but the cheaper first move may be deleting unused dependencies and delaying initialization. AOT and CRaC are powerful; they are not substitutes for a lean boot path.

For serverless-style or scale-to-zero Java, startup becomes part of product latency — then CDS, native image, or checkpoint/restore move from interesting to necessary. For a long-lived monolith that restarts monthly, spend energy on steady-state SLOs first. Fit the tool to the deployment model, the same way we fitted collectors to SLOs.

Ways to improve startup, said as an engineer: reduce classpath and initialization work first, use CDS or AppCDS where it pays, lean on lazy and deliberate lifecycle init, and consider native image or checkpoint/restore when the deployment model demands fast bring-up. Doing heavy work in static initializers and shipping enormous classpaths are the mistakes that make exotic tools look necessary before you have earned them.

We closed the JVM's life cycle from cold start through steady-state pauses. The remaining gap is telling that arc as one coherent interview story — from load to diagnosis — without buzzword bingo.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — JVM Startup (Episode 65).

Narration technique: steady-state vs cold start → classloading/init → three clocks → CDS/AOT/CRaC → classpath → fit to deployment model → bridge to interview wrap.

Teaching points preserved: classloading/verification/init; CDS/AppCDS; AOT/native image; CRaC; lazy init carefully.
