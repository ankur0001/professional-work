# Episode 55 — JIT Compilation

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Four showed the garbage collector reclaiming heap objects. But how does bytecode actually run at full speed? The JVM starts with an interpreter — executing opcodes one by one.

Hot methods get compiled to native machine code by the JIT compiler. C1 compiles fast with basic optimizations — C2 compiles deep and slow. Today — JIT compilation, tiered execution, and deoptimization.

Episode Fifty-Five. JIT Compilation. The interpreter executes bytecode without ahead-of-time compilation. Every method starts in interpreted mode — simple, portable, slower. The JVM profiles execution — counting loop iterations and method calls.

Profiling data feeds the JIT — identifying hot code paths. Cold code stays interpreted — no compilation overhead wasted. Interpretation is the safety net when compiled code becomes invalid.

Tiered compilation uses multiple JIT compilers. C1 — client compiler — fast compile, basic optimizations, quick warmup. C2 — server compiler — slow compile, aggressive inlining and loop opts.

Default on modern JDK — methods escalate from interpreted to C1 to C2. Compilation happens on background threads — application keeps running. Compiled code lives in code cache — native memory separate from heap.

A method becomes hot when invocation or loop counters exceed thresholds. CompileThreshold and tiered thresholds control when compilation triggers. Inlining replaces method calls with the callee body — huge speedup.

Escape analysis can stack-allocate objects that never leave the method. Dead code elimination and constant folding happen at compile time. Profile-guided optimization uses runtime data for better code generation.

Deoptimization reverts compiled code back to the interpreter. Happens when assumptions break — new class loaded, uncommon trap hit. Uncommon traps guard speculative optimizations like monomorphic calls.

The JVM patches call sites and re-enters interpreted mode safely. Recompilation may follow with updated profiling data. Deoptimization is normal — not a bug — it preserves correctness.

The tiered execution pipeline in order. Level zero — pure interpretation with profiling. Level one — C1 compiled without profiling overhead. Level two and three — C1 with increasing profiling detail.

Level four — C2 fully optimized native code. Understanding tiers helps interpret JIT compilation log output. Three common mistakes. One — disabling tiered compilation without measuring — rarely helps.

Two — assuming first-run performance equals steady-state — warmup matters. Three — micro-benchmarking without JVM warmup — measures interpreter only. Also — printing deoptimization events in production without understanding them.

Benchmark with warmup iterations — let the JIT compile before timing. Interview question — how does the JVM JIT work? Bytecode starts interpreted — profiler counts hot methods. C1 fast compile with basic opts — C2 deep optimize for hot code.

Inlining, escape analysis, and loop unrolling at compile time. Deoptimization when assumptions fail — revert to interpreter. Warmup matters — steady-state performance differs from cold start.

GC and JIT both shape runtime performance — collectors differ wildly. Episode Fifty-Six — GC Collectors. Serial, Parallel, G1, ZGC — and when to choose each. See you there.
