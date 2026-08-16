# Episode 45 — BlockingQueue

| Field | Value |
|---|---|
| Episode | 45 |
| Title | BlockingQueue |
| Catalog handbook column | 45 |
| Narration source script | `make_episode_45.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Producers generate work. Consumers process it. They run at different speeds.
2. A shared list without bounds lets producers outpace consumers — memory explodes.
3. BlockingQueue adds capacity limits and blocking put and take semantics.
4. When full, put waits. When empty, take waits. Natural backpressure.
5. The producer-consumer pattern is the backbone of thread pools and pipelines.
6. Today — BlockingQueue, the pattern, and choosing the right implementation.

### Scene `title` (renderer: `title`)

1. Episode Forty-Five.
2. BlockingQueue and Producer-Consumer.

### Scene `blocking_queue` (renderer: `blocking_queue`)

1. BlockingQueue extends Queue with blocking operations.
2. put inserts an element — blocks if the queue is full.
3. take removes an element — blocks if the queue is empty.
4. offer and poll provide timed or non-blocking alternatives.
5. Thread-safe — multiple producers and consumers without external locks.
6. The queue itself coordinates waiting and waking threads.

### Scene `producer_consumer` (renderer: `producer_consumer`)

1. Producer-consumer decouples creation from processing.
2. Producers enqueue tasks — consumers dequeue and execute.
3. Bounded queue caps in-flight work — protects memory and downstream systems.
4. ExecutorService thread pools use internal work queues this way.
5. Pipeline stages connect via queues — each stage runs at its own pace.
6. Backpressure emerges naturally when the queue fills.

### Scene `array_blocking` (renderer: `array_blocking`)

1. ArrayBlockingQueue uses a fixed-capacity circular array.
2. One lock for both put and take — simple and predictable.
3. Fair ordering optional — FIFO for waiting threads.
4. Bounded capacity set at construction — cannot grow.
5. Low overhead for steady workloads with known bounds.
6. Choose when you need a fixed-size buffer with array backing.

### Scene `linked_blocking` (renderer: `linked_blocking`)

1. LinkedBlockingQueue uses linked nodes — optionally bounded.
2. Two locks — one for put, one for take — better under mixed load.
3. Default capacity is Integer.MAX_VALUE — effectively unbounded.
4. Always pass an explicit capacity in production — unbounded queues hide leaks.
5. Higher memory per element than array — but no upfront array allocation.
6. Common in executor frameworks when capacity is configured explicitly.

### Scene `when_blocking` (renderer: `when_blocking`)

1. When to use BlockingQueue.
2. Thread pool work queues — bounded backpressure.
3. Log or event pipelines — producers spike, consumers steady.
4. Handoff between stages — parse, transform, persist.
5. Replace wait-notify handoffs with a cleaner API.
6. When not — single-threaded batch — a simple List suffices.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — unbounded LinkedBlockingQueue — memory grows under slow consumers.
3. Two — put without handling InterruptedException — shutdown breaks cleanly.
4. Three — multiple consumers on one queue without coordination — usually fine, but watch ordering.
5. Also — blocking take on the only thread that should stop the pipeline.
6. Size the queue — too small starves workers, too large hides overload.

### Scene `interview` (renderer: `interview`)

1. Interview question — why BlockingQueue over synchronized List?
2. Built-in blocking put and take — no manual wait-notify loops.
3. Bounded capacity provides backpressure automatically.
4. Thread-safe for multiple producers and consumers.
5. ArrayBlockingQueue — fixed array, one lock. Linked — dual locks.
6. Mention producer-consumer and ExecutorService work queues.

### Scene `teaser` (renderer: `teaser`)

1. Queues pass work between threads. What about composing async results?
2. Episode Forty-Six — CompletableFuture Deep Dive.
3. thenApply, thenCompose, allOf, and exception handling.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **45** — *BlockingQueue*.
- **Series catalog:** Episode 45 ↔ handbook lesson 45 — *BlockingQueue*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Producers generate work. Consumers process it. They run at different speeds._
- **`title`** — starts from: _Episode Forty-Five._
- **`blocking_queue`** — starts from: _BlockingQueue extends Queue with blocking operations._
- **`producer_consumer`** — starts from: _Producer-consumer decouples creation from processing._
- **`array_blocking`** — starts from: _ArrayBlockingQueue uses a fixed-capacity circular array._
- **`linked_blocking`** — starts from: _LinkedBlockingQueue uses linked nodes — optionally bounded._
- **`when_blocking`** — starts from: _When to use BlockingQueue._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why BlockingQueue over synchronized List?_
- **`teaser`** — starts from: _Queues pass work between threads. What about composing async results?_
