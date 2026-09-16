# Episode 45 — BlockingQueue

**Cut:** v1 (original)

## Transcript (from captions)

Producers generate work. Consumers process it. They run at different speeds. A shared list without bounds lets producers outpace consumers — memory explodes. BlockingQueue adds capacity limits and blocking put and take semantics.

When full, put waits. When empty, take waits. Natural backpressure. The producer-consumer pattern is the backbone of thread pools and pipelines. Today — BlockingQueue, the pattern, and choosing the right implementation.

Episode Forty-Five. BlockingQueue and Producer-Consumer. BlockingQueue extends Queue with blocking operations. put inserts an element — blocks if the queue is full. take removes an element — blocks if the queue is empty.

offer and poll provide timed or non-blocking alternatives. Thread-safe — multiple producers and consumers without external locks. The queue itself coordinates waiting and waking threads.

Producer-consumer decouples creation from processing. Producers enqueue tasks — consumers dequeue and execute. Bounded queue caps in-flight work — protects memory and downstream systems.

ExecutorService thread pools use internal work queues this way. Pipeline stages connect via queues — each stage runs at its own pace. Backpressure emerges naturally when the queue fills.

ArrayBlockingQueue uses a fixed-capacity circular array. One lock for both put and take — simple and predictable. Fair ordering optional — FIFO for waiting threads. Bounded capacity set at construction — cannot grow.

Low overhead for steady workloads with known bounds. Choose when you need a fixed-size buffer with array backing. LinkedBlockingQueue uses linked nodes — optionally bounded. Two locks — one for put, one for take — better under mixed load.

Default capacity is Integer.MAX_VALUE — effectively unbounded. Always pass an explicit capacity in production — unbounded queues hide leaks. Higher memory per element than array — but no upfront array allocation.

Common in executor frameworks when capacity is configured explicitly. When to use BlockingQueue. Thread pool work queues — bounded backpressure. Log or event pipelines — producers spike, consumers steady.

Handoff between stages — parse, transform, persist. Replace wait-notify handoffs with a cleaner API. When not — single-threaded batch — a simple List suffices. Three common mistakes.

One — unbounded LinkedBlockingQueue — memory grows under slow consumers. Two — put without handling InterruptedException — shutdown breaks cleanly. Three — multiple consumers on one queue without coordination — usually fine, but watch ordering.

Also — blocking take on the only thread that should stop the pipeline. Size the queue — too small starves workers, too large hides overload. Interview question — why BlockingQueue over synchronized List?

Built-in blocking put and take — no manual wait-notify loops. Bounded capacity provides backpressure automatically. Thread-safe for multiple producers and consumers. ArrayBlockingQueue — fixed array, one lock. Linked — dual locks.

Mention producer-consumer and ExecutorService work queues. Queues pass work between threads. What about composing async results? Episode Forty-Six — CompletableFuture Deep Dive. thenApply, thenCompose, allOf, and exception handling.

See you there.
