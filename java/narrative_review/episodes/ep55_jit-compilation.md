# Episode 55 — JIT Compilation

| Field | Value |
|---|---|
| Episode | 55 |
| Title | JIT Compilation |
| Catalog handbook column | 55 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Four showed the garbage collector reclaiming unreachable heap objects.
2. But how does bytecode actually run at full speed after startup?
3. The JVM starts with an interpreter — executing opcodes one by one, collecting profiling data.
4. Hot methods get compiled to native machine code by the JIT compiler — just-in-time, not ahead-of-time for app code.
5. C1 compiles fast with basic optimizations — C2 compiles deep and slow with aggressive inlining.
6. Today — JIT compilation, tiered execution, and deoptimization when assumptions break.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Five.
2. JIT Compilation.
3. We'll follow the tier pipeline, name hot methods, and explain why your first benchmark lap lies.

### Scene `interpreter` (renderer: `interpreter`)

1. The interpreter executes bytecode without ahead-of-time native compilation for application methods.
2. Every method starts in interpreted mode — simple, portable, slower per invocation — collects invocation and loop counters.
3. The JVM profiles execution — which methods run often, which loops spin millions of iterations.
4. Profiling data feeds the JIT — identifying hot code paths worth compiling to native instructions.
5. Cold code stays interpreted — no compilation overhead wasted on startup-only configuration paths.
6. Interpretation is the safety net when compiled code becomes invalid — deoptimization lands back here.

### Scene `c1_c2` (renderer: `c1_c2`)

1. Tiered compilation uses multiple JIT compilers — C1 client, C2 server on HotSpot.
2. C1 — fast compile, basic optimizations, quick warmup — good enough for medium-hot code.
3. C2 — slow compile, aggressive inlining, loop unrolling, escape analysis — peak steady-state performance.
4. Default on modern JDK — methods escalate from interpreted to C1 to C2 as counters cross thresholds.
5. Compilation happens on background compiler threads — application keeps running during compiles, mostly.
6. Compiled native code lives in code cache — native memory separate from Java heap — CodeCache full is a real failure mode.

### Scene `hot_methods` (renderer: `hot_methods`)

1. A method becomes hot when invocation or loop counters exceed CompileThreshold — JVM-specific, tunable.
2. Inlining replaces callee bodies into caller native code — eliminates call overhead, enables further opts.
3. Escape analysis can eliminate allocations for non-escaping objects — stack allocate or scalar replace at C2.
4. Dead code elimination and constant folding happen at compile time — bytecode not equal to native instructions executed.
5. Profile-guided optimization uses runtime branch frequencies — layout hot paths for instruction cache friendliness.
6. Watch this — micro-benchmarks that never warm up measure interpreter fiction, not production steady state.

```java
public static long sum(int[] data) {
    long total = 0;
    for (int v : data) total += v;  // hot loop → C2 may vectorize or unroll
    return total;
}
```

7. Run that loop billions of times in a server — JIT cares. Run once in a unit test — interpreter only.

### Scene `deoptimization` (renderer: `deoptimization`)

1. Deoptimization reverts compiled native code back to interpreter when assumptions break.
2. Happens when new class loads invalidate monomorphic call sites — uncommon trap to interpreter path.
3. Uncommon traps guard speculative optimizations — assumed one implementation, reality loaded another subclass.
4. JVM patches call sites and re-enters interpreted mode safely — correctness preserved, performance dips temporarily.
5. Recompilation may follow with updated profiling — cycle repeats as code evolves.
6. Deoptimization is normal — not a bug — it preserves Java semantics under dynamic class loading.

### Scene `compilation_tiers` (renderer: `compilation_tiers`)

1. The tiered execution pipeline in order — useful when reading -XX:+PrintCompilation logs.
2. Level zero — pure interpretation with profiling counters active.
3. Level one — C1 compiled without full profiling overhead — quick native path.
4. Levels two and three — C1 with increasing profiling detail — stepping stone to C2.
5. Level four — C2 fully optimized native code — what you want for hot server loops after warmup.
6. Understanding tiers explains why first requests after deploy feel slow — cold interpreter, empty code cache.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — disabling tiered compilation without measuring — rarely helps modern workloads, often hurts warmup.
3. Mistake two — assuming first-run performance equals steady-state — warmup iterations mandatory for honest benchmarks.
4. Mistake three — micro-benchmarking with JMH but zero warmup forks — still measures cold code if misconfigured.
5. Also — printing deoptimization floods in production without understanding — noise unless investigating class loading issues.
6. Benchmark with warmup — let JIT compile before timing — JMH handles this when used correctly.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: How does the JVM JIT work?
3. Answer: Bytecode starts interpreted — profiler counts hot methods and loops.
4. C1 fast compile with basic opts — C2 deep optimize with inlining, escape analysis, loop transforms for hot code.
5. Deoptimization when assumptions fail — new classes, uncommon branches — revert to interpreter safely.
6. Warmup matters — steady-state performance differs from cold start — mention tiered compilation pipeline.
7. Connect to Episode Fifty-Nine escape analysis — shows JVM story hangs together.

### Scene `teaser` (renderer: `teaser`)

1. GC and JIT both shape runtime performance — but collectors differ wildly in pause behavior.
2. Episode Fifty-Six — GC Collectors.
3. Serial, Parallel, G1, ZGC — and when to choose each for your workload.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **55** — *JIT Compilation*.
- **Series catalog:** Episode 55 ↔ handbook lesson 55 — *JIT Compilation*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with hot-loop JIT example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — interpreter vs native speed path
- **`title`** — episode title card
- **`interpreter`** — profiling and cold start
- **`c1_c2`** — tiered compilers and code cache
- **`hot_methods`** — inlining and profile-guided opts
- **`deoptimization`** — uncommon traps and reversion
- **`compilation_tiers`** — level 0–4 pipeline
- **`mistakes`** — cold benchmarks, disabling tiered comp
- **`interview`** — JIT workflow interview answer
- **`teaser`** — bridge to GC Collectors
