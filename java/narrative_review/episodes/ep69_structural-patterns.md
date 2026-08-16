# Episode 69 — Structural Patterns

| Field | Value |
|---|---|
| Episode | 69 |
| Title | Structural Patterns |
| Catalog handbook column | 69 |
| Narration source script | `make_episode_69.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Eight covered creational patterns — how objects are born.
2. Structural patterns cover how objects and classes compose into larger structures.
3. APIs rarely match perfectly — you adapt, wrap, and simplify interfaces constantly.
4. java.io is a masterclass in Decorator — wrappers adding buffering and encoding.
5. Facades and proxies appear in every service layer and remote call path.
6. Today — Adapter, Decorator, Facade, Proxy, and Composite.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Nine.
2. Structural Patterns.

### Scene `adapter` (renderer: `adapter`)

1. Adapter converts one interface into another clients expect.
2. You have a useful class — its method names or types do not match callers.
3. Write a thin adapter that delegates — callers stay clean and testable.
4. Object adapters compose — class adapters inherit — prefer composition in Java.
5. JDK — Arrays.asList adapts an array to the List interface.
6. Adapter is integration glue — keep it thin and obvious.

### Scene `decorator` (renderer: `decorator`)

1. Decorator attaches responsibilities dynamically by wrapping.
2. Same interface as the core object — transparent to callers.
3. Stack wrappers — buffer, then encrypt, then compress — open for extension.
4. java.io InputStream hierarchy is the textbook Java Decorator example.
5. Unlike inheritance trees, decoration mixes features without combinatorial subclasses.
6. Watch the stack depth — too many wrappers obscure debugging.

### Scene `facade` (renderer: `facade`)

1. Facade provides a simple interface to a complex subsystem.
2. Subsystem classes remain available — facade is a convenience entry point.
3. Service layers often act as facades over repositories, clients, and mappers.
4. SLF4J over logging backends is a facade-style boundary.
5. Facades reduce coupling — clients depend on one door, not twenty rooms.
6. Do not let a facade become a god object — keep it a thin orchestrator.

### Scene `proxy` (renderer: `proxy`)

1. Proxy controls access to another object with the same interface.
2. Virtual proxy — lazy creation — remote proxy — network boundary — protection proxy — auth.
3. Java dynamic proxies and Spring AOP wrap beans for transactions and security.
4. Unlike Decorator, Proxy's purpose is access control, not adding features.
5. Caching proxies memoize expensive calls transparently.
6. Know why the proxy exists — latency, security, laziness, or logging.

### Scene `composite` (renderer: `composite`)

1. Composite treats individual objects and compositions uniformly.
2. Trees of nodes — files and folders, UI widgets, expression trees.
3. Clients call the same operations on leaves and composites.
4. Great for recursive structures — awkward when children differ wildly in API.
5. Watch the Liskov risks — not every operation makes sense on every node.
6. Use Composite when hierarchy and uniform treatment are real requirements.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Adapter that grows business logic — keep adapters thin.
3. Two — Decorator stacks nobody can debug — document the wrap order.
4. Three — Facade that hides too much — teams reopen the subsystem anyway.
5. Also — calling every wrapper a Proxy — purpose differs from Decorator.
6. Structure should clarify boundaries — not invent new ones for sport.

### Scene `interview` (renderer: `interview`)

1. Interview question — Decorator versus Proxy — how do they differ?
2. Both wrap an object and usually share its interface.
3. Decorator adds or alters behavior — buffering, logging, compression.
4. Proxy controls access — lazy init, remote call, authorization, caching.
5. In Spring, AOP proxies often implement cross-cutting access concerns.
6. Name the intent first — feature stacking versus access control.

### Scene `teaser` (renderer: `teaser`)

1. Structure connects objects — behavior connects collaborations.
2. Episode Seventy — Behavioral Patterns.
3. Strategy, Observer, Command, Template Method, and Iterator.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **69** — *Structural Patterns*.
- **Series catalog:** Episode 69 ↔ handbook lesson 69 — *Structural Patterns*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Eight covered creational patterns — how objects are born._
- **`title`** — starts from: _Episode Sixty-Nine._
- **`adapter`** — starts from: _Adapter converts one interface into another clients expect._
- **`decorator`** — starts from: _Decorator attaches responsibilities dynamically by wrapping._
- **`facade`** — starts from: _Facade provides a simple interface to a complex subsystem._
- **`proxy`** — starts from: _Proxy controls access to another object with the same interface._
- **`composite`** — starts from: _Composite treats individual objects and compositions uniformly._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Decorator versus Proxy — how do they differ?_
- **`teaser`** — starts from: _Structure connects objects — behavior connects collaborations._
