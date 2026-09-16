# Episode 106 — Layered Architecture

| Field | Value |
|---|---|
| Episode | 106 |
| Title | Layered Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 106 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Before fancy architectures, most teams start with layers. Layered architecture is the baseline map.

Here is the pain this lesson exists to remove. Without layers: SQL in controllers, entities exposed as JSON, untestable god classes, circular dependencies between packages.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Layered Architecture.

Layered Architecture (n-tier) organizes Spring applications into horizontal layers with strict dependency direction : upper layers depend on lower layers, never the reverse.

A little context helps the idea stick. Layered architecture predates Spring (1990s enterprise patterns). Spring's @Controller/@Service/@Repository stereotypes encode layers explicitly. Criticism: anemic domain model if all logic in services.

Spring's design choice here is deliberate. Stereotypes + component scan + package-by-layer conventions make structure enforceable with ArchUnit.

Once you accept the feature, the next honest question is how it works under the hood. Same IoC container — layers are package/bean organization, not separate contexts.

Let's make this concrete with a small example you can read aloud and still follow.

```java
HTTP → Controller → Service → Repository → Database
 │ │
 DTO @Entity (map at boundary)
```

Read it top to bottom once. Notice what your code declares versus what the framework takes over. The point of Spring is rarely "more annotations." The point is fewer decisions you must reinvent on every project.

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Layered Architecture inside Phase 12 — Enterprise Architecture. The next natural question is waiting in Episode 107 — Hexagonal Architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 106 (*Layered Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
