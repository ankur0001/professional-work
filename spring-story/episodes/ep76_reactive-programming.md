# Episode 76 — Reactive Programming

| Field | Value |
|---|---|
| Episode | 76 |
| Title | Reactive Programming |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 76 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Threads waiting on I/O do not scale forever. Reactive programming rethinks how work is scheduled.

Here is the pain this lesson exists to remove. Thread-per-request model breaks at ~10K concurrent connections — memory for stacks, context switching. Reactive model scales I/O-bound apps with fixed thread pools. Complexity cost: debugging, stack traces, learning curve.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Reactive Programming.

Reactive Programming is a programming paradigm oriented around asynchronous data streams and non-blocking execution. Instead of one thread blocked per request waiting for I/O, a small pool of threads handles many concurrent operations via event loops and callbacks/pipelines.

A little context helps the idea stick. Reactive Streams spec (2013). Spring Boot 2 reactive support. Virtual threads (Java 21) now offer alternative for blocking code at scale — architect trade-off.

Spring's design choice here is deliberate. Unified programming model: same DI, same Boot, WebClient for reactive HTTP, R2DBC for reactive SQL. Interop with blocking via subscribeOn(Schedulers.boundedElastic()) when needed.

Once you accept the feature, the next honest question is how it works under the hood. Reactor operators build operator chains (lazy until subscribe). Netty under WebFlux — no Servlet API. DispatcherHandler replaces DispatcherServlet for routing.

As you practice Reactive Programming, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Reactive Programming inside Phase 8 — Reactive Spring. The next natural question is waiting in Episode 77 — Mono.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 76 (*Reactive Programming*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
