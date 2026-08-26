# Episode 67 — Design Patterns Intro

| Field | Value |
|---|---|
| Episode | 67 |
| Title | Design Patterns Intro |
| Catalog handbook column | 67 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The JVM arc taught you what happens under a running program. Now shift the camera. Two teammates argue about a redesign. One says, "We need a Strategy here." The other says, "That is just an interface." A third says, "Patterns are outdated — use Spring." They are missing a shared definition. Design patterns are shared vocabulary for recurring design problems — context, forces, and trade-offs — not stamps you smash onto every class to sound senior.

```java
// Pattern = named solution to a recurring design problem
// Use when the problem actually recurs
```

A pattern is useful when the problem actually recurs — when naming it saves meeting time. If the problem appears once, a clear function may beat a named pattern. Prefer clarity. Do not pattern-paint simple code.

Start from a situation. You are building pricing rules. Today there is one rule. Tomorrow marketing wants seasonal, loyalty, and partner discounts. Nested conditionals grow. Someone proposes a Strategy hierarchy; someone else a switch; someone else a rules engine. The conversation is not "which buzzword?" It is "what problem are we solving, what trade-offs do we accept, and will the next person recognize this shape?" Context plus problem plus trade-offs — that is how catalogs like Gang of Four earned their keep. Named experience, not holy scripture.

Hold a second situation beside pricing. You inherit a payment integration duplicated in three modules with different timeouts and retries. Someone says "Adapter." Someone says "Facade." Someone says "just copy the best one into a util." Vocabulary helps only if you can say: we need one curated door over a messy subsystem — facade energy — or we need to translate a foreign interface into our port — adapter energy. Without the problem statement, pattern names become team theater.

Language features can replace some classical patterns. A Java `enum` with methods can replace certain constant-heavy singletons. Lambdas shrink some Strategy boilerplate. Records shrink tiny data carriers. Modules and DI containers change how factories appear. That does not make patterns outdated. Catalogs evolve; naming recurring structures still helps. Before lambdas, Strategy often meant a named class per variant; after, many Strategies become a one-liner — same idea, thinner ceremony. "Patterns are outdated" is too blunt; "always use the GoF book literally" is too blunt the other way.

Read patterns as tools in a drawer. You reach for a wrench when a bolt needs turning — not empty the drawer onto every repair. Factory methods help when creation deserves a name. Decorators help when you add behavior without exploding subclasses. Observers help when many listeners react to an event. Force a pattern where a straightforward class would do and you pay indirection tax without gaining vocabulary.

Watch how pattern talk goes wrong. Someone labels every interface a Strategy. Someone introduces an AbstractFactory for two concrete types that will never multiply. The cure is the same discipline we used for JVM flags: name the symptom, name the trade-off, then choose the tool. Teach a three-question gate before merging a pattern: What recurs? What trade-off do we accept? What simpler language feature did we consider first? If those answers are thin, keep the clear code and drop the pattern name from the PR.

A healthy team uses pattern names as compression. "This is a facade over the payment SDK" communicates intent faster than a five-minute tour — if everyone shares the meaning. Misleading names are worse than no names.

In interviews, when asked whether patterns still matter, answer with team compression and evolving catalogs: one example where a language feature replaced a classical shape, and one where naming Strategy or Decorator still clarifies a review.

Today we demystified patterns as vocabulary under constraints. Next we get concrete with creational patterns — how objects come to life, where singletons go wrong, when builders beat telescoping constructors, and how containers often own lifecycle in modern Java.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Design Patterns Intro (Episode 67).

Narration technique: teammate vocabulary clash → patterns as named recurring solutions → pricing + payment situations → language features evolve catalogs → tools not stamps → three-question gate → bridge to creational.

Teaching points preserved: context/problem/trade-offs; language features replace some patterns; prefer clarity; don't pattern-paint; read as tools.
