# Episode 68 — Creational Patterns

| Field | Value |
|---|---|
| Episode | 68 |
| Title | Creational Patterns |
| Catalog handbook column | 68 |
| Narration source script | `make_episode_68.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Seven introduced design patterns and the three GoF categories.
2. Creational patterns answer one question — who creates objects, and how.
3. Scattered new keywords couple callers to concrete classes and construction details.
4. When construction grows complex — optional fields, validation, families of products — patterns help.
5. Java codebases lean on Factory and Builder constantly — Singleton less often than people think.
6. Today — Singleton, Factory Method, Abstract Factory, Builder, and Prototype.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Eight.
2. Creational Patterns.

### Scene `singleton` (renderer: `singleton`)

1. Singleton ensures one instance with a global access point.
2. Classic use — a shared configuration or a process-wide registry.
3. In Java — prefer enum singleton or static holder for thread-safe lazy init.
4. Cost — hidden global state that complicates testing and parallel evolution.
5. Dependency injection often replaces Singleton — inject one instance instead of reaching for it.
6. Reach for Singleton only when truly one is required — not as a default.

### Scene `factory` (renderer: `factory`)

1. Factory Method lets subclasses decide which concrete type to create.
2. Callers depend on an interface — not on new ConcreteThing parentheses.
3. Abstract Factory builds families of related products that must stay consistent.
4. Example — UI kits with matching buttons and dialogs per look and feel.
5. JDK examples — Collection iterators, Charset encoders, JDBC DriverManager.
6. Factories shine when creation rules change more often than usage sites.

### Scene `builder` (renderer: `builder`)

1. Builder constructs complex objects step by step with a fluent API.
2. Telescoping constructors — many overloads — become unreadable fast.
3. Builder sets fields, validates, then builds an immutable result.
4. Java records and Lombok builders are modern flavors of the same idea.
5. StringBuilder is a specialized builder for character sequences.
6. Use Builder when objects have many optional parameters or invariant checks.

### Scene `prototype` (renderer: `prototype`)

1. Prototype creates new objects by copying a prototypical instance.
2. Useful when construction is expensive or configuration is mostly shared.
3. Java's Cloneable is awkward — prefer copy constructors or copy factories.
4. Deep versus shallow copy matters — shared mutable state surprises teams.
5. Deserialization and object pools sometimes play a similar role.
6. Prototype is rarer in Java apps — know it, use it when cloning beats rebuilding.

### Scene `choose` (renderer: `choose`)

1. How to choose among creational patterns.
2. One shared instance — Singleton or better, a DI-managed bean.
3. Vary the type created — Factory Method or a simple static factory.
4. Many optional fields — Builder with validation at build time.
5. Families of products — Abstract Factory keeps combinations consistent.
6. Start with a static factory method — escalate only when forces demand it.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Singleton as a service locator for everything — testing nightmare.
3. Two — Abstract Factory for a single product type — unnecessary hierarchy.
4. Three — mutable builders reused across threads without care.
5. Also — Cloneable without documenting deep versus shallow semantics.
6. Creation should clarify ownership — not hide it.

### Scene `interview` (renderer: `interview`)

1. Interview question — Factory versus Builder — when each?
2. Factory chooses which type to instantiate — hides concrete classes.
3. Builder assembles one complex object — many optional fields, clear validation.
4. Factory returns quickly — Builder chains setters then builds.
5. They combine — a factory may return a preconfigured builder.
6. Pick the one that matches the force — type variation versus construction complexity.

### Scene `teaser` (renderer: `teaser`)

1. Creation is settled — next is composition.
2. Episode Sixty-Nine — Structural Patterns.
3. Adapter, Decorator, Facade, Proxy, and Composite.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **68** — *JVM Tuning*.
- **Series catalog mapping:** Episode 68 / catalog column `68` / published title *Creational Patterns*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Seven introduced design patterns and the three GoF categories._
- **`title`** — starts from: _Episode Sixty-Eight._
- **`singleton`** — starts from: _Singleton ensures one instance with a global access point._
- **`factory`** — starts from: _Factory Method lets subclasses decide which concrete type to create._
- **`builder`** — starts from: _Builder constructs complex objects step by step with a fluent API._
- **`prototype`** — starts from: _Prototype creates new objects by copying a prototypical instance._
- **`choose`** — starts from: _How to choose among creational patterns._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Factory versus Builder — when each?_
- **`teaser`** — starts from: _Creation is settled — next is composition._
