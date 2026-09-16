# Episode 50 — Virtual Threads

**Cut:** v1 (original)

## Transcript (from captions)

Episode Forty-Nine showed how platform threads deadlock under bad lock order. Platform threads are expensive — one megabyte stack, OS scheduling overhead. A web server handling ten thousand concurrent requests cannot spawn ten thousand threads.

Project Loom brings virtual threads — lightweight, JVM-managed, millions per process. Block on I/O and the carrier thread serves another virtual thread. Today — virtual threads, pinning, and an intro to structured concurrency.

Episode Fifty. Virtual Threads — Project Loom. Project Loom reimagined threads without rewriting your Java code. Virtual threads are cheap — create with Thread.startVirtualThread or Executors.newVirtualThreadPerTaskExecutor.

The JVM multiplexes many virtual threads onto few platform carrier threads. Blocking I/O unmounts the virtual thread — carrier runs another. Same Thread API — Runnable, Callable, synchronized — mostly unchanged.

Shipped as a preview in Java 19, finalized in Java 21. Platform thread — one-to-one with an OS thread. Virtual thread — many-to-one on carrier pool threads. Platform threads suit CPU-bound parallel work — limited by cores.

Virtual threads suit I/O-bound concurrency — waiting on network or disk. Do not pool virtual threads — create one per task, they are cheap. Do pool platform threads or use ForkJoinPool for CPU parallelism.

Pinning — when a virtual thread cannot unmount from its carrier. synchronized blocks may pin — carrier stuck until monitor released. Native code or JNI can pin — carrier blocked in native layer.

Long CPU work on a virtual thread pins the carrier — hurts throughput. Prefer ReentrantLock over synchronized for hot paths with virtual threads. Monitor jfr events or thread dumps for pinned carrier warnings.

Structured concurrency — scope owns child tasks, cancels on failure. StructuredTaskScope in preview — fork subtasks, join or shutdown on error. Parent lifetime bounds children — no orphaned background work.

ShutdownOnFailure — first exception cancels siblings. ShutdownOnSuccess — first success cancels the rest. Pairs naturally with virtual threads — cheap fan-out and clean teardown. When virtual threads shine.

HTTP servers — one virtual thread per request blocking on I/O. Database calls, REST clients, file reads — classic blocking APIs. Replace reactive frameworks only when simplicity beats throughput tuning.

When not — heavy CPU computation — use platform threads or ForkJoinPool. When not — massive synchronized hot paths — pinning negates benefits. Three common mistakes. One — pooling virtual threads — unnecessary, create per task.

Two — CPU-bound work on virtual threads — pins carriers. Three — ignoring synchronized pinning — switch to ReentrantLock. Also — thread-local assumptions with millions of virtual threads.

Virtual threads change scale — not every old pattern still fits. Interview question — virtual threads versus platform threads? Virtual — lightweight, JVM-scheduled, millions possible, great for I/O.

Platform — OS thread, heavier, best for CPU-bound parallelism. Blocking unmounts virtual thread — carrier serves another. Pinning from synchronized or native code blocks the carrier.

Mention Java 21 finalization and structured concurrency preview. Threads run code — but where does that code come from? Episode Fifty-One — Class Loading Basics. ClassLoader hierarchy, linkage, and initialization.

See you there.
