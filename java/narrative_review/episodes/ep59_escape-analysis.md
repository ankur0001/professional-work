# Episode 59 — Escape Analysis

| Field | Value |
|---|---|
| Episode | 59 |
| Title | Escape Analysis |
| Catalog handbook column | 59 |
| Narration source script | `make_episode_59.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Eight showed jcmd, jmap, and JFR for live diagnostics.
2. But the JIT compiler makes invisible optimizations before runtime tools see them.
3. Escape analysis asks — does this object leave the current scope?
4. If not, the JVM may never allocate it on the heap at all.
5. Stack allocation and scalar replacement eliminate heap pressure silently.
6. Today — escape analysis, stack allocation, and when objects escape.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Nine.
2. Escape Analysis.

### Scene `escape_definition` (renderer: `escape_definition`)

1. An object escapes when a reference outlives the creating method or thread.
2. Returned from a method — escapes to the caller.
3. Stored in a field or static variable — escapes to the object graph.
4. Passed to another thread — escapes across thread boundaries.
5. Published to a collection visible elsewhere — escapes globally.
6. No escape means the JIT can treat the object as method-local only.

### Scene `stack_allocation` (renderer: `stack_allocation`)

1. Stack allocation places short-lived objects on the thread stack frame.
2. Avoids heap allocation and GC pressure entirely for non-escaping objects.
3. The object dies when the stack frame pops — no collector involvement.
4. Enabled by escape analysis during C2 compilation.
5. You cannot observe stack allocation directly — it is a compiler optimization.
6. Micro-benchmarks with millions of tiny allocations may show zero GC impact.

### Scene `scalar_replacement` (renderer: `scalar_replacement`)

1. Scalar replacement goes further — the object may not exist at all.
2. Fields of a non-escaping object become local variables in registers.
3. No object header, no alignment padding — just primitive values.
4. Point class with int x and int y — replaced by two local ints.
5. Combines with dead code elimination and constant folding.
6. Most powerful when objects are small and method-local.

### Scene `escape_scenarios` (renderer: `escape_scenarios`)

1. When does escape analysis fail to optimize?
2. Returning the object — always escapes to the caller heap.
3. Storing in an instance field — escapes with the enclosing object.
4. Synchronized blocks publishing to shared state — escapes globally.
5. Logging or debug toString that captures references — subtle escape.
6. Inlining boundaries — if callee escapes, caller object may escape too.

### Scene `jit_flags` (renderer: `jit_flags`)

1. Observing escape analysis in practice.
2. C2 compiler performs escape analysis by default — no flag needed.
3. PrintCompilation shows when methods reach C2 optimized level.
4. JITWatch and -XX:+PrintInlining reveal inlining decisions.
5. Async Profiler allocation samples drop when optimizations kick in after warmup.
6. Do not disable escape analysis in production — it is a core C2 optimization.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — assuming every new creates a heap object — escape analysis may elide it.
3. Two — benchmarking without warmup — measures interpreter, not optimized code.
4. Three — storing objects in fields to avoid allocation — guarantees escape.
5. Also — relying on object identity for non-escaping locals — may be scalar-replaced.
6. Write clear, short-lived objects — let the JIT optimize naturally.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is escape analysis?
2. JIT analyzes whether object references leave method or thread scope.
3. No escape — stack allocate or scalar replace fields into locals.
4. Escapes on return, field store, or cross-thread publish.
5. Reduces allocation rate and GC pressure invisibly at C2 compile time.
6. Warmup required — optimization appears after hot method compilation.

### Scene `teaser` (renderer: `teaser`)

1. Heap objects are only part of JVM memory — classes and native buffers live elsewhere.
2. Episode Sixty — Metaspace and Native Memory.
3. Metaspace versus PermGen, direct buffers, and NMT.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **59** — *Escape Analysis*.
- **Series catalog:** Episode 59 ↔ handbook lesson 59 — *Escape Analysis*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Eight showed jcmd, jmap, and JFR for live diagnostics._
- **`title`** — starts from: _Episode Fifty-Nine._
- **`escape_definition`** — starts from: _An object escapes when a reference outlives the creating method or thread._
- **`stack_allocation`** — starts from: _Stack allocation places short-lived objects on the thread stack frame._
- **`scalar_replacement`** — starts from: _Scalar replacement goes further — the object may not exist at all._
- **`escape_scenarios`** — starts from: _When does escape analysis fail to optimize?_
- **`jit_flags`** — starts from: _Observing escape analysis in practice._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is escape analysis?_
- **`teaser`** — starts from: _Heap objects are only part of JVM memory — classes and native buffers live elsewhere._
