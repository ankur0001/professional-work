# Episode 50 — Virtual Threads

| Field | Value |
|---|---|
| Episode | 50 |
| Title | Virtual Threads |
| Catalog handbook column | 50 |
| Narration source script | `make_episode_50.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Forty-Nine showed how platform threads deadlock under bad lock order.
2. Platform threads are expensive — one megabyte stack, OS scheduling overhead.
3. A web server handling ten thousand concurrent requests cannot spawn ten thousand threads.
4. Project Loom brings virtual threads — lightweight, JVM-managed, millions per process.
5. Block on I/O and the carrier thread serves another virtual thread.
6. Today — virtual threads, pinning, and an intro to structured concurrency.

### Scene `title` (renderer: `title`)

1. Episode Fifty.
2. Virtual Threads — Project Loom.

### Scene `project_loom` (renderer: `project_loom`)

1. Project Loom reimagined threads without rewriting your Java code.
2. Virtual threads are cheap — create with Thread.startVirtualThread or Executors.newVirtualThreadPerTaskExecutor.
3. The JVM multiplexes many virtual threads onto few platform carrier threads.
4. Blocking I/O unmounts the virtual thread — carrier runs another.
5. Same Thread API — Runnable, Callable, synchronized — mostly unchanged.
6. Shipped as a preview in Java 19, finalized in Java 21.

### Scene `virtual_vs_platform` (renderer: `virtual_vs_platform`)

1. Platform thread — one-to-one with an OS thread.
2. Virtual thread — many-to-one on carrier pool threads.
3. Platform threads suit CPU-bound parallel work — limited by cores.
4. Virtual threads suit I/O-bound concurrency — waiting on network or disk.
5. Do not pool virtual threads — create one per task, they are cheap.
6. Do pool platform threads or use ForkJoinPool for CPU parallelism.

### Scene `pinning` (renderer: `pinning`)

1. Pinning — when a virtual thread cannot unmount from its carrier.
2. synchronized blocks may pin — carrier stuck until monitor released.
3. Native code or JNI can pin — carrier blocked in native layer.
4. Long CPU work on a virtual thread pins the carrier — hurts throughput.
5. Prefer ReentrantLock over synchronized for hot paths with virtual threads.
6. Monitor jfr events or thread dumps for pinned carrier warnings.

### Scene `structured_concurrency` (renderer: `structured_concurrency`)

1. Structured concurrency — scope owns child tasks, cancels on failure.
2. StructuredTaskScope in preview — fork subtasks, join or shutdown on error.
3. Parent lifetime bounds children — no orphaned background work.
4. ShutdownOnFailure — first exception cancels siblings.
5. ShutdownOnSuccess — first success cancels the rest.
6. Pairs naturally with virtual threads — cheap fan-out and clean teardown.

### Scene `when_to_use` (renderer: `when_to_use`)

1. When virtual threads shine.
2. HTTP servers — one virtual thread per request blocking on I/O.
3. Database calls, REST clients, file reads — classic blocking APIs.
4. Replace reactive frameworks only when simplicity beats throughput tuning.
5. When not — heavy CPU computation — use platform threads or ForkJoinPool.
6. When not — massive synchronized hot paths — pinning negates benefits.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — pooling virtual threads — unnecessary, create per task.
3. Two — CPU-bound work on virtual threads — pins carriers.
4. Three — ignoring synchronized pinning — switch to ReentrantLock.
5. Also — thread-local assumptions with millions of virtual threads.
6. Virtual threads change scale — not every old pattern still fits.

### Scene `interview` (renderer: `interview`)

1. Interview question — virtual threads versus platform threads?
2. Virtual — lightweight, JVM-scheduled, millions possible, great for I/O.
3. Platform — OS thread, heavier, best for CPU-bound parallelism.
4. Blocking unmounts virtual thread — carrier serves another.
5. Pinning from synchronized or native code blocks the carrier.
6. Mention Java 21 finalization and structured concurrency preview.

### Scene `teaser` (renderer: `teaser`)

1. Threads run code — but where does that code come from?
2. Episode Fifty-One — Class Loading Basics.
3. ClassLoader hierarchy, linkage, and initialization.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **50** — *Virtual Threads*.
- **Series catalog:** Episode 50 ↔ handbook lesson 50 — *Virtual Threads*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Forty-Nine showed how platform threads deadlock under bad lock order._
- **`title`** — starts from: _Episode Fifty._
- **`project_loom`** — starts from: _Project Loom reimagined threads without rewriting your Java code._
- **`virtual_vs_platform`** — starts from: _Platform thread — one-to-one with an OS thread._
- **`pinning`** — starts from: _Pinning — when a virtual thread cannot unmount from its carrier._
- **`structured_concurrency`** — starts from: _Structured concurrency — scope owns child tasks, cancels on failure._
- **`when_to_use`** — starts from: _When virtual threads shine._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — virtual threads versus platform threads?_
- **`teaser`** — starts from: _Threads run code — but where does that code come from?_
