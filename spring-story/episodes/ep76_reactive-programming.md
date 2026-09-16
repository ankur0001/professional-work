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

Here is the pain this lesson exists to remove. Problem Statement Thread-per-request model breaks at ~10K concurrent connections — memory for stacks, context switching. Reactive model scales I/O-bound apps with fixed thread pools. Complexity cost: debugging, stack traces, learning curve.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Reactive Programming.

Concept Reactive Programming is a programming paradigm oriented around asynchronous data streams and non-blocking execution. Instead of one thread blocked per request waiting for I/O, a small pool of threads handles many concurrent operations via event loops and callbacks/pipelines.

Spring's design choice here is deliberate. Interop with blocking via subscribeOn(Schedulers.boundedElastic()) when needed. Design Principles Behind Spring Principle How Spring Applies It Inversion of Control Container controls object creation and wiring Dependency Injection Dependencies supplied via constructor/setter/field Separation of Concerns Config, cross-cutting (AOP), and domain logic separated Program to Interfaces Beans wired by type/name; swap impls without code change Convention over Configuration Boot defaults; sensible @Component scanning Non-invasive No framework classes required in domain model (POJOs) Spring vs Solving It Yourself Custom DI container Spring Framework

Once you accept the feature, the next honest question is how it works under the hood. Internal Working Reactor operators build operator chains (lazy until subscribe). Netty under WebFlux — no Servlet API. DispatcherHandler replaces DispatcherServlet for routing. Container Refresh Sequence (High Level) Application startup

As you practice Reactive Programming, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Reactive Programming inside Phase 8 — Reactive Spring. The next natural question is waiting in Episode 77 — Mono.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 76 (*Reactive Programming*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
