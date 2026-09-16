# Episode 59 — Escape Analysis

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Eight showed jcmd, jmap, and JFR for live diagnostics. But the JIT compiler makes invisible optimizations before runtime tools see them. Escape analysis asks — does this object leave the current scope?

If not, the JVM may never allocate it on the heap at all. Stack allocation and scalar replacement eliminate heap pressure silently. Today — escape analysis, stack allocation, and when objects escape.

Episode Fifty-Nine. Escape Analysis. An object escapes when a reference outlives the creating method or thread. Returned from a method — escapes to the caller. Stored in a field or static variable — escapes to the object graph.

Passed to another thread — escapes across thread boundaries. Published to a collection visible elsewhere — escapes globally. No escape means the JIT can treat the object as method-local only.

Stack allocation places short-lived objects on the thread stack frame. Avoids heap allocation and GC pressure entirely for non-escaping objects. The object dies when the stack frame pops — no collector involvement.

Enabled by escape analysis during C2 compilation. You cannot observe stack allocation directly — it is a compiler optimization. Micro-benchmarks with millions of tiny allocations may show zero GC impact.

Scalar replacement goes further — the object may not exist at all. Fields of a non-escaping object become local variables in registers. No object header, no alignment padding — just primitive values.

Point class with int x and int y — replaced by two local ints. Combines with dead code elimination and constant folding. Most powerful when objects are small and method-local. When does escape analysis fail to optimize?

Returning the object — always escapes to the caller heap. Storing in an instance field — escapes with the enclosing object. Synchronized blocks publishing to shared state — escapes globally.

Logging or debug toString that captures references — subtle escape. Inlining boundaries — if callee escapes, caller object may escape too. Observing escape analysis in practice. C2 compiler performs escape analysis by default — no flag needed.

PrintCompilation shows when methods reach C2 optimized level. JITWatch and -XX:+PrintInlining reveal inlining decisions. Async Profiler allocation samples drop when optimizations kick in after warmup.

Do not disable escape analysis in production — it is a core C2 optimization. Three common mistakes. One — assuming every new creates a heap object — escape analysis may elide it. Two — benchmarking without warmup — measures interpreter, not optimized code.

Three — storing objects in fields to avoid allocation — guarantees escape. Also — relying on object identity for non-escaping locals — may be scalar-replaced. Write clear, short-lived objects — let the JIT optimize naturally.

Interview question — what is escape analysis? JIT analyzes whether object references leave method or thread scope. No escape — stack allocate or scalar replace fields into locals. Escapes on return, field store, or cross-thread publish.

Reduces allocation rate and GC pressure invisibly at C2 compile time. Warmup required — optimization appears after hot method compilation. Heap objects are only part of JVM memory — classes and native buffers live elsewhere.

Episode Sixty — Metaspace and Native Memory. Metaspace versus PermGen, direct buffers, and NMT. See you there.
