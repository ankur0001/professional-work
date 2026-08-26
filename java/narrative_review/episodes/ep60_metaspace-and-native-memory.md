# Episode 60 — Metaspace and Native Memory

| Field | Value |
|---|---|
| Episode | 60 |
| Title | Metaspace and Native Memory |
| Catalog handbook column | 60 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Two already whispered a warning: do not equate Java memory with `-Xmx`. By now we have lived inside the heap — collectors, leaks, dumps — so it is easy to forget that warning. Then production serves a cruel demo. The process is killed. The heap dump you scramble to take shows free space. Monitoring says old gen was fine. The container's OOMKiller does not care about your heap chart. Something outside the heap exhausted the budget, and the kernel ended the argument.

So the natural question is: if `-Xmx` is not the process size, what else counts?

Metaspace holds class metadata — the JVM's data about classes and classloaders, not your instance fields. Load many classes, generate proxies, spin up scripting engines, hot-reload carelessly, and metaspace grows. A classloader leak does not only retain heap objects; it can pin metadata until metaspace pressure becomes the incident. That is why "we still had heap" and "metaspace was huge" can be the same outage told from two angles. Unlimited metaspace with rogue loaders is not flexibility. It is a slow fuse with a polite heap graph.

Native memory is a broader umbrella. Thread stacks consume native memory for every thread you start — and virtual threads change the economics, but platform threads still matter in mixed systems. Direct byte buffers allocate off-heap for I/O paths that want to avoid extra copies. JNI libraries bring their own allocations that Java code cannot see in a heap dump. GC implementations keep native structures. The code cache holds JIT-compiled methods. Compressed oops and other internals have costs. None of that is billed to `-Xmx`, yet all of it lives inside the process — and inside a container memory limit if you are running in one.

Watch a common misconfiguration:

```bash
java -Xmx512m -XX:MaxMetaspaceSize=256m -jar app.jar
# still leave room for threads/native/direct buffers
```

Someone sees a 768 megabyte container and sets `-Xmx` to 768m, or sets heap plus metaspace equal to the limit with no headroom. Threads start. Direct buffers appear. Native GC structures appear. The cgroup limit is hit while the heap still looks polite. Setting `-Xmx` equal to the container limit is one of the most popular ways to create mysterious OOMs. Headroom is not waste. Headroom is admitting the process is larger than its heap.

Direct memory deserves its own glare. NIO and many networking stacks love direct buffers for good reasons. Without a bound and without visibility, direct memory becomes a silent second heap. Ignoring it is how teams stare at heap graphs while off-heap climbs and RSS tells a different story. Native Memory Tracking — NMT — helps attribute native usage when you need to prove where the bytes went. You would not leave the most detailed tracking on forever without cost awareness, but when RSS disagrees with heap, NMT is how you stop shrugging.

Connect this back to Episode Fifty-Seven. If loaders cannot unload, metaspace trends upward across redeploys. Cap metaspace when you need a tripwire that fails fast instead of growing forever. Fix the leak. Leave container headroom for stacks, direct buffers, code cache, and GC native memory. The operational habit is simple to say and often skipped: compare process RSS and cgroup usage to heap usage before you retune the collector.

So why can a JVM die with free heap? Because native memory, metaspace, stacks, direct buffers, and container limits live beyond `-Xmx`. Say that in an interview, then say how you would confirm: compare RSS or cgroup usage to heap, check metaspace growth, inspect direct buffer metrics, enable NMT when needed, and look for loader growth across redeploys. Dying with free heap is not a paradox. It is a reminder that the heap is one account in a larger bank.

We widened memory from "the heap" to "the process." Next we return to the heap with more precision: soft, weak, and phantom references — ways to cooperate with GC for caches and cleanup without pretending reachability is only strong-or-gone. That is Episode Sixty-One.

Walk a container story end to end. Limit is 1Gi. Someone sets `-Xmx768m` and feels conservative. The service uses hundreds of threads, each with a stack. Netty burns direct memory. Metaspace sits at 150m after proxy generation. RSS crosses the limit while heap used is 500m. The on-call engineer opens heap charts first and loses an hour. The correct first comparison is process memory versus heap memory. If they diverge, leave the collector alone until native and metaspace are ruled out.

Direct buffers have another failure mode: the heap looks fine, `OutOfMemoryError: Direct buffer memory` appears, and the team has never set `-XX:MaxDirectMemorySize` or monitored `BufferPool` metrics. Ignoring direct memory is not neutral. It is choosing blindness in systems that live on NIO.

Walk a container story end to end. Limit is 1Gi. Someone sets `-Xmx768m` and feels conservative. The service uses hundreds of threads, each with a stack. Netty burns direct memory. Metaspace sits at 150m after proxy generation. RSS crosses the limit while heap used is 500m. The on-call engineer opens heap charts first and loses an hour. The correct first comparison is process memory versus heap memory. If they diverge, leave the collector alone until native and metaspace are ruled out.

Direct buffers have another failure mode: the heap looks fine, `OutOfMemoryError: Direct buffer memory` appears, and the team has never set `-XX:MaxDirectMemorySize` or monitored `BufferPool` metrics. Ignoring direct memory is not neutral. It is choosing blindness in systems that live on NIO.

Classloader leaks also show up when framework hot reload is used in environments that were never meant to reload forever. Each reload that fails to release the old loader adds a metaspace step. Eventually the step function becomes an outage. The dump may show heap retained by the loader, or metaspace may trip first. Either way, the lifetime bug is the same family as Episode Fifty-Seven — a reference that outlived its intended scope.

Classloader leaks also show up when framework hot reload is used in environments that were never meant to reload forever. Each reload that fails to release the old loader adds a metaspace step. Eventually the step function becomes an outage. The dump may show heap retained by the loader, or metaspace may trip first. Either way, the lifetime bug is the same family as Episode Fifty-Seven — a reference that outlived its intended scope.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Metaspace and Native Memory (Episode 60).

Narration technique: OOM with free heap → what else counts → metaspace → native umbrella → container headroom command → direct memory + NMT → classloader/metaspace → interview woven → bridge to reference types.

Teaching points preserved: metaspace; direct buffers/stacks/JNI/GC native; container headroom; NMT; classloader leaks in metaspace.
