# Episode 55 — JIT Compilation

| Field | Value |
|---|---|
| Episode | 55 |
| Title | JIT Compilation |
| Catalog handbook column | 55 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Garbage collection explained how the heap stays livable. Another reason Java can feel "slow then fast" sits on the CPU side of the runtime. The first calls to a method may run in the interpreter. As a method gets hot, the Just-In-Time compiler turns it into optimized native code. Warmup is not folklore. It is the pipeline.

The JIT turns hot interpreted code into optimized native code after warmup. First requests can be slow because of loading, interpretation, and compilation. Steady-state matters for servers — and for honest benchmarks.

```java
// first calls may be slow (warmup)
// steady-state matters for servers
for (int i = 0; i < 100_000; i++) {
    hotPath(i);
}
```

Walk the intuition. Early iterations may interpret `hotPath`. Profiling decides it is hot. Compilers — often talked about as C1 and C2 tiers — produce native code with increasing optimization investment. C1 tends to be quicker, lighter compilation; C2 invests more for heavier optimization on truly hot code. Exact tier policy evolves, but the idea stays: pay compile cost where it pays back in run time.

Deoptimization happens when speculative optimizations assume something that later proves false — a class hierarchy that changes, a rare branch that appears, an optimistic inlining decision that stops being valid. The JVM can fall back and recompile. That flexibility is why the JIT can optimize aggressively. It is also why microbenchmarks that ignore warmup and deopt behavior lie.

Warmup affects benchmarks. Timing a method once at startup measures class loading, interpretation, and compile overhead as much as the algorithm. Servers care about steady-state latency after warmup — and also about warmup itself when autoscaling brings cold instances into a load balancer. Both stories are real; they are not the same measurement.

Use JMH for microbenchmarks when you need micro-truth. JMH handles warmup iterations, forks, and measurement modes that casual `System.nanoTime` loops get wrong. Optimizing cold code you saw in a single local run is a classic waste: you rearrange something the JIT would have inlined or eliminated anyway after warmup.

```text
cold start → load classes, interpret, compile
warm → run optimized native code
assumption breaks → deoptimize, maybe recompile
```

What if we assume the JIT always makes everything fastest immediately?

Then we are surprised by cold starts, and we publish benchmarks that never reached steady state. What if we micro-optimize a getter the profiler barely sees? Then we ignore allocation and algorithm costs that dominate. The JIT is powerful. It is not a substitute for measuring the right phase of the right workload.

Why is the first request slow? Loading + interpretation + JIT warmup — plus whatever I/O your application does. That interview answer is today's episode in one line. The deeper craft is knowing when to care about warmup, when to care about steady state, and when to care about allocation and GC instead of instruction-level panic.

Tiered compilation exists so the JVM does not pay C2's compile cost for methods that run twice. Short-lived CLI tools may barely warm. Long-lived servers live in the warm world — until a new instance scales out cold. Feature flags that flip a rarely used path into a hot path can also cause compile waves mid-day. JIT is adaptive to the profile it sees, not to the profile you assumed in January.

Deoptimization is not failure; it is honesty. When a speculative inline stops being valid, continuing would be incorrect. The pause or slowdown from deopt can surprise latency charts. If you see weird warm-path spikes after a class load or megamorphic call site change, keep deopt in the differential diagnosis.

What if a blog shows a 10x microbenchmark win from a rewrite that JMH cannot reproduce with proper warmup? Believe JMH. Casual timers are how myths spread. The JIT already performs miracles; your job is to measure them, not to invent them from cold runs.

Hold a practical checklist: interpret then compile hot paths; respect warmup in benchmarks and in capacity planning; expect deoptimization when profiles change; use JMH for micro claims; optimize what profiles show after steady state. Meet those and JIT becomes a partner you can reason with.

Across this JVM mini-arc — loaders, bytecode, stack/heap, GC, JIT — each episode answered a question the previous one created. That is the same narrative discipline as the language episodes, applied to the runtime under your program.

Picture an autoscale event that adds cold JVMs behind a load balancer. The first minutes show higher latency while classes load and hot methods compile. A warmup policy — synthetic traffic before taking production, or gradual ramp — is an operations answer to a JIT fact. Ignoring warmup and blaming "Java is slow" misunderstands the runtime you chose.

Picture a microbenchmark that "proves" a rewrite is 20x faster by timing one call. JMH with warmup disagrees. Believe the methodology that matches how servers actually run.

So reconnect the chain. Hot methods earn native code. Tiers and deoptimization explain adaptive optimization. Warmup separates cold from steady. JMH and humility keep measurements honest. Across Episodes Fifty-One through Fifty-Five we walked from how classes arrive, through bytecode and memory, to GC and JIT — a progressive JVM picture without pretending one episode can hold every flag.

The next episodes continue that arc into collectors, leaks, diagnostics, and deeper optimizations. For now, notice the pattern that has guided the whole series: each tool appeared because the previous story created a problem you could feel.

That curiosity — not a flag encyclopedia — is how JVM knowledge stays useful.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 55 (*JIT Compilation*).

Narration technique: slow-then-fast situation → interpreter then JIT → C1/C2 tiers → deopt → warmup/JMH → mistakes → bridge beyond EP55.
