# Episode 45 — BlockingQueue

| Field | Value |
|---|---|
| Episode | 45 |
| Title | BlockingQueue |
| Catalog handbook column | 45 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Synchronizers coordinate phases. Producer/consumer pipelines coordinate flow. One side creates jobs; the other side processes them. If producers sprint ahead without a brake, memory fills with queued work until the process dies. If consumers spin forever checking a list, you waste CPU. So the natural question is: what structure hands off work, waits when empty, and pushes back when full?

Blocking queues are the backbone of producer/consumer designs. `put` and `take` block. `offer` and `poll` can time out or fail fast depending on the overload. Bounded queues apply backpressure so producers cannot crash the process with unbounded growth.

```java
BlockingQueue<Job> q = new ArrayBlockingQueue<>(100);
q.put(job);
Job j = q.take();
```

Walk it. The queue holds at most one hundred jobs. A producer blocks in `put` when the queue is full — that block is backpressure. A consumer blocks in `take` when the queue is empty — that block is patience without busy spin. The queue is the meeting place. Producers and consumers need not know each other's identities; they need a shared queue and a shutdown protocol.

Why bound the queue? Because an unbounded queue turns a slow consumer into an out-of-memory incident. Bounding makes overload visible as blocking or rejection instead of silent heap growth. Interviewers ask this because the wrong default feels convenient in demos and lethal in production.

Variants exist for different needs. `ArrayBlockingQueue` is bounded and array-backed. `LinkedBlockingQueue` can be bounded or left unbounded if you pass no capacity — know which you chose. `PriorityBlockingQueue` orders by priority instead of plain FIFO. Choose the variant for the ordering and bounding story you mean, not for the class name you saw first.

Shutdown needs a protocol. One common pattern is a poison pill — a special job that means "stop." Another is interrupting consumers and letting them exit. Another is draining and shutting down an executor that owns the consumers. No shutdown protocol means threads waiting in `take` forever after the rest of the app wants to die.

```java
private static final Job POISON = new Job("STOP");

// producer finally:
q.put(POISON);

// consumer:
Job j = q.take();
if (j == POISON) {
    break;
}
```

Pair queues with executors thoughtfully. Often consumers are pool workers that `take` from a queue, or the executor's own internal queue is the handoff. Understand which queue you are bounding — the one you created, or the one hiding inside `newFixedThreadPool`. Hidden unbounded queues are still unbounded.

What if we busy-spin instead of `take`?

```java
while (true) {
    Job j = q.poll();
    if (j != null) process(j);
}
```

When empty, this burns a core. Blocking exists so waiting is cheap. Poll with timeout can be valid when you must wake periodically; pure spin is rarely the design you meant.

Backpressure is easiest to feel with numbers. Capacity 100 means the 101st `put` waits. Waiting producers slow the intake. That slowdown is information: the system is saturated. An unbounded queue converts the same saturation into rising heap usage until GC thrashes or the process dies. Prefer the symptom you can operate on — blocked puts, rejected offers, visible queue depth — over the symptom that pages you with an OOM at midnight.

`offer` and `poll` with timeouts give hybrid policies: try for a while, then take an alternate path such as rejecting a user request or shedding load. Not every producer should block forever. Boundedness gives you the right to choose.

Pairing with executors needs ownership clarity. If the executor already has an internal queue, adding another blocking queue in front may be double buffering without a plan. Sometimes that is intentional staging; sometimes it is accidental complexity. Draw the diagram of who blocks whom before you ship.

Priority queues change fairness: urgent jobs jump ahead. That helps deadlines and hurts starvation if low priority work never runs. Boundedness still applies — a priority queue full of urgent work can still exhaust memory if unbounded, and can still block producers if bounded. Priority is an ordering policy inside the capacity story, not a replacement for capacity.
Document the shutdown pill carefully when multiple producers exist; only one poison may not stop every consumer, and multiple pills may be required. Protocols are part of the queue's API even when they are application-level conventions.

Picture an image-processing pipeline: upload threads put jobs into a bounded queue of 200; four worker threads take and process. When the queue fills, uploads block or reject. Operators watch queue depth. That visible pressure is healthier than an unbounded list silently holding ten thousand pending images in heap. The blocking queue is not only a data structure — it is an operational control surface.

If you remember one line: bound the queue to make overload visible. Visibility beats silent growth. Consumers should `take` or timed `poll`, not spin. Producers should have a shutdown story that does not strand waiters.

Hold the checklist: capacity chosen from memory and latency budgets; consumers blocking without spin; producers handling full queues with policy; shutdown that wakes waiters. Meet those four and BlockingQueue stops being scary vocabulary and becomes ordinary plumbing.

So reconnect the chain. Fast producers and slow consumers forced a handoff structure. Blocking queues provided put/take, bounded backpressure, and variants for ordering. Poison pills and executor pairing sketched shutdown and architecture. Unbounded queues and busy spins showed the failure modes.

Once handoffs and pools feel familiar, the next hunger is composing asynchronous stages — transform this result, then combine with that other call, with timeouts and error recovery along the graph.

Episode Forty-Six: `CompletableFuture`.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 45 (*BlockingQueue*).

Narration technique: producer/consumer pressure → BlockingQueue → bound/backpressure → variants → poison pill → executor pairing → busy-spin mistake → next natural problem (CompletableFuture).
