# Episode 67 — Design Patterns Intro

| Field | Value |
|---|---|
| Episode | 67 |
| Title | Design Patterns Intro |
| Catalog handbook column | 67 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The JVM arc taught you what happens under a running program. Now shift the camera. Two teammates argue about a redesign. One says, "We need a Strategy here." The other says, "That is just an interface." A third says, "Patterns are outdated — use Spring." They are not speaking different truths so much as missing a shared definition. Design patterns are shared vocabulary for recurring design problems — context, forces, and trade-offs — not stamps you smash onto every class to sound senior.

```java
// Pattern = named solution to a recurring design problem
// Use when the problem actually recurs
```

That comment is the whole thesis in miniature. A pattern is useful when the problem actually recurs — when you have seen the same shape enough times that naming it saves meeting time. If the problem appears once, a clear function may beat a named pattern. Prefer clarity. Do not pattern-paint simple code.

Start from a situation. You are building pricing rules. Today there is one rule. Tomorrow marketing wants seasonal discounts, loyalty discounts, and partner discounts. Nested conditionals grow. Someone proposes a Strategy hierarchy. Someone else proposes a switch. Someone else proposes a rules engine. The pattern conversation is not "which buzzword?" It is "what problem are we solving, what trade-offs do we accept, and will the next person recognize this shape?" Context plus problem plus trade-offs — that is how catalogs like Gang of Four earned their keep. They were never holy scripture. They were named experience.

Language features can replace some classical patterns. A Java `enum` with methods can replace certain constant-heavy singletons. Lambdas and method references shrink some Strategy boilerplate. Records shrink some tiny data carriers that used to become hand-written value objects. Modules and dependency injection containers change how factories appear in enterprise code. That does not make patterns outdated. Catalogs evolve; naming recurring structures still helps teams. The question "are patterns outdated?" deserves an answer like that — evolution, not funeral.

Read patterns as tools in a drawer. You do not empty the drawer onto every repair. You reach for a wrench when a bolt needs turning. Factory methods help when creation logic deserves a name. Decorators help when you must add behavior without exploding subclasses. Observers help when many listeners react to an event. If you force a pattern where a straightforward class would do, you pay indirection tax without gaining vocabulary. Using patterns to sound smart is the social version of the same mistake.

Watch how pattern talk goes wrong in interviews and reviews. Someone labels every interface a Strategy. Someone introduces an AbstractFactory for two concrete types that will never multiply. Someone refuses a simple decorator because "we should use AOP." The cure is the same discipline we used for JVM flags: name the symptom, name the trade-off, then choose the tool. If you cannot say what problem recurs, you are not ready to name a pattern.

A healthy team uses pattern names as compression. "This is a facade over the payment SDK" communicates intent faster than a five-minute tour of classes — if everyone shares the meaning. New teammates learn faster when the codebase's real patterns match the names in comments and design docs. Misleading names are worse than no names.

So what should you take into the next episodes? Not a mandate to sprinkle patterns everywhere. A habit: when a design problem starts repeating, ask whether a named structure already exists for it. Then ask whether modern Java or your framework already provides a sharper tool. Prefer the clearest option that preserves change room.

Hold a second situation beside pricing. You inherit a payment integration duplicated in three modules: different timeouts, different retry counts, different log formats. Someone says "Adapter." Someone says "Facade." Someone says "just copy the best one into a util." The vocabulary helps only if you can say: we need one curated door over a messy subsystem — that is facade energy — or we need to translate a foreign interface into our port — that is adapter energy. Without the problem statement, pattern names become team theater.

Java's evolution keeps rewriting the catalog's surface. Before lambdas, Strategy often meant a named class file per variant. After lambdas, many Strategies become a one-liner at the call site — still the same idea, thinner ceremony. Before records, tiny immutable carriers begged for boilerplate; records removed a reason to invent a micro-pattern for data holders. Before DI containers, factories and service locators carried more weight in application code. The underlying problems — vary behavior, assemble structure, control creation — remain. The default Java tool for each problem shifts. That is why "patterns are outdated" is too blunt, and "always use the GoF book literally" is too blunt the other way.

Teach juniors a three-question gate before merging a pattern. What recurs? What trade-off do we accept — indirection, more types, more flexibility? What simpler language feature did we consider first? If those answers are thin, delete the pattern name from the PR description and keep the clear code.

In interviews, you may be asked whether patterns still matter. Answer with team compression and evolving catalogs, then give one example where a language feature replaced a classical shape, and one example where naming Strategy or Decorator still clarifies a review. That balanced answer sounds like experience.

Today we demystified patterns as vocabulary under constraints. Next we get concrete with creational patterns — how objects come to life, where singletons go wrong, when builders beat telescoping constructors, and how containers often own lifecycle in modern Java. That is Episode Sixty-Eight.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Design Patterns Intro (Episode 67).

Narration technique: teammate vocabulary clash → patterns as named recurring solutions → pricing situation → language features evolve catalogs → tools not stamps → interview/review failure modes → bridge to creational.

Teaching points preserved: context/problem/trade-offs; language features replace some patterns; prefer clarity; don't pattern-paint; read as tools.
