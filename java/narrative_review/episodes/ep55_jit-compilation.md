# Episode 55 — JIT Compilation

| Field | Value |
|---|---|
| Episode | 55 |
| Title | JIT Compilation |
| Catalog handbook column | 55 |
| Narration source script | `make_episode_55.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Four showed the garbage collector reclaiming heap objects.
2. But how does bytecode actually run at full speed?
3. The JVM starts with an interpreter — executing opcodes one by one.
4. Hot methods get compiled to native machine code by the JIT compiler.
5. C1 compiles fast with basic optimizations — C2 compiles deep and slow.
6. Today — JIT compilation, tiered execution, and deoptimization.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Five.
2. JIT Compilation.

### Scene `interpreter` (renderer: `interpreter`)

1. The interpreter executes bytecode without ahead-of-time compilation.
2. Every method starts in interpreted mode — simple, portable, slower.
3. The JVM profiles execution — counting loop iterations and method calls.
4. Profiling data feeds the JIT — identifying hot code paths.
5. Cold code stays interpreted — no compilation overhead wasted.
6. Interpretation is the safety net when compiled code becomes invalid.

### Scene `c1_c2` (renderer: `c1_c2`)

1. Tiered compilation uses multiple JIT compilers.
2. C1 — client compiler — fast compile, basic optimizations, quick warmup.
3. C2 — server compiler — slow compile, aggressive inlining and loop opts.
4. Default on modern JDK — methods escalate from interpreted to C1 to C2.
5. Compilation happens on background threads — application keeps running.
6. Compiled code lives in code cache — native memory separate from heap.

### Scene `hot_methods` (renderer: `hot_methods`)

1. A method becomes hot when invocation or loop counters exceed thresholds.
2. CompileThreshold and tiered thresholds control when compilation triggers.
3. Inlining replaces method calls with the callee body — huge speedup.
4. Escape analysis can stack-allocate objects that never leave the method.
5. Dead code elimination and constant folding happen at compile time.
6. Profile-guided optimization uses runtime data for better code generation.

### Scene `deoptimization` (renderer: `deoptimization`)

1. Deoptimization reverts compiled code back to the interpreter.
2. Happens when assumptions break — new class loaded, uncommon trap hit.
3. Uncommon traps guard speculative optimizations like monomorphic calls.
4. The JVM patches call sites and re-enters interpreted mode safely.
5. Recompilation may follow with updated profiling data.
6. Deoptimization is normal — not a bug — it preserves correctness.

### Scene `compilation_tiers` (renderer: `compilation_tiers`)

1. The tiered execution pipeline in order.
2. Level zero — pure interpretation with profiling.
3. Level one — C1 compiled without profiling overhead.
4. Level two and three — C1 with increasing profiling detail.
5. Level four — C2 fully optimized native code.
6. Understanding tiers helps interpret JIT compilation log output.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — disabling tiered compilation without measuring — rarely helps.
3. Two — assuming first-run performance equals steady-state — warmup matters.
4. Three — micro-benchmarking without JVM warmup — measures interpreter only.
5. Also — printing deoptimization events in production without understanding them.
6. Benchmark with warmup iterations — let the JIT compile before timing.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does the JVM JIT work?
2. Bytecode starts interpreted — profiler counts hot methods.
3. C1 fast compile with basic opts — C2 deep optimize for hot code.
4. Inlining, escape analysis, and loop unrolling at compile time.
5. Deoptimization when assumptions fail — revert to interpreter.
6. Warmup matters — steady-state performance differs from cold start.

### Scene `teaser` (renderer: `teaser`)

1. GC and JIT both shape runtime performance — collectors differ wildly.
2. Episode Fifty-Six — GC Collectors.
3. Serial, Parallel, G1, ZGC — and when to choose each.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **55** — *JIT Compilation*.
- **Series catalog:** Episode 55 ↔ handbook lesson 55 — *JIT Compilation*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Four showed the garbage collector reclaiming heap objects._
- **`title`** — starts from: _Episode Fifty-Five._
- **`interpreter`** — starts from: _The interpreter executes bytecode without ahead-of-time compilation._
- **`c1_c2`** — starts from: _Tiered compilation uses multiple JIT compilers._
- **`hot_methods`** — starts from: _A method becomes hot when invocation or loop counters exceed thresholds._
- **`deoptimization`** — starts from: _Deoptimization reverts compiled code back to the interpreter._
- **`compilation_tiers`** — starts from: _The tiered execution pipeline in order._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does the JVM JIT work?_
- **`teaser`** — starts from: _GC and JIT both shape runtime performance — collectors differ wildly._
