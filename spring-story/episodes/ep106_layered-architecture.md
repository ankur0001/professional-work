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

Here is the pain this lesson exists to remove. Problem Statement Without layers: SQL in controllers, entities exposed as JSON, untestable god classes, circular dependencies between packages.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Layered Architecture.

Concept Layered Architecture (n-tier) organizes Spring applications into horizontal layers with strict dependency direction : upper layers depend on lower layers, never the reverse.

Spring's design choice here is deliberate. Why Spring Provides This Feature Stereotypes + component scan + package-by-layer conventions make structure enforceable with ArchUnit. Design Principles Behind Spring Principle How Spring Applies It Inversion of Control Container controls object creation and wiring Dependency Injection Dependencies supplied via constructor/setter/field Separation of Concerns Config, cross-cutting (AOP), and domain logic separated Program to Interfaces Beans wired by type/name; swap impls without code change Convention over Configuration Boot defaults; sensible @Component scanning Non-invasive No framework classes required in domain model (POJOs) Spring vs Solving It Yourself Custom DI container Spring Framework

Once you accept the feature, the next honest question is how it works under the hood. Internal Working Same IoC container — layers are package/bean organization, not separate contexts. Container Refresh Sequence (High Level) Application startup

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
