# Episode 70 — Behavioral Patterns

| Field | Value |
|---|---|
| Episode | 70 |
| Title | Behavioral Patterns |
| Catalog handbook column | 70 |
| Narration source script | `make_episode_70.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Nine covered structural patterns — adapting, wrapping, and composing.
2. Behavioral patterns focus on algorithms and communication between objects.
3. They let you vary what happens without rewriting call sites every time.
4. Strategy swaps algorithms — Observer broadcasts events — Command queues actions.
5. These patterns dominate service code and interview whiteboards alike.
6. Today — Strategy, Observer, Command, Template Method, and Iterator — then Spring next.

### Scene `title` (renderer: `title`)

1. Episode Seventy.
2. Behavioral Patterns.

### Scene `strategy` (renderer: `strategy`)

1. Strategy defines a family of algorithms and makes them interchangeable.
2. Clients depend on a strategy interface — concrete strategies plug in.
3. Comparator in Java is Strategy — sort order injected at call time.
4. Payment processors, pricing rules, and retry policies are classic Strategies.
5. Prefer Strategy over deep if-else chains that grow every quarter.
6. Keep strategies focused — one decision axis per strategy type.

### Scene `observer` (renderer: `observer`)

1. Observer notifies dependents automatically when a subject changes.
2. Publish-subscribe and event listeners are Observer in modern clothes.
3. Swing listeners, reactive streams, and message topics follow the shape.
4. Decouples producers from consumers — but watch notification storms.
5. Unregister carefully — leaked listeners are memory leak classics.
6. Use Observer when many parties care about the same state change.

### Scene `command` (renderer: `command`)

1. Command encapsulates a request as an object.
2. You can queue, log, undo, and retry actions uniformly.
3. Runnable and Callable are lightweight command shapes in Java.
4. GUI actions, job queues, and transactional outboxes use Command ideas.
5. Macro commands compose smaller commands into workflows.
6. Command separates invoker from receiver — great for undo stacks.

### Scene `template_iterator` (renderer: `template_iterator`)

1. Template Method defines an algorithm skeleton in a base class.
2. Subclasses override steps without changing the overall sequence.
3. JdbcTemplate and many framework hooks follow Template Method spirit.
4. Iterator provides sequential access without exposing collection structure.
5. Enhanced for-loops and Stream pipelines rest on Iterator ideas.
6. Together they show behavior reuse — hooks and traversal, not inheritance for data.

### Scene `choose` (renderer: `choose`)

1. Choosing behavioral patterns in practice.
2. Vary an algorithm — Strategy or a simple function parameter.
3. Broadcast state changes — Observer or an event bus with clear ownership.
4. Queue or undo work — Command objects with explicit lifecycle.
5. Framework-defined steps — Template Method or modern composition hooks.
6. Prefer small interfaces — behavioral patterns should shrink switch statements.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Strategy explosion — dozens of one-line classes for dead branches.
3. Two — Observer spaghetti — unclear who listens and who owns cleanup.
4. Three — Command without idempotency — retries double-charge users.
5. Also — Template Method locking teams into brittle inheritance.
6. Behavior patterns need ownership rules — not just class diagrams.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do Strategy and Template Method differ?
2. Strategy composes algorithms via interfaces — swap at runtime.
3. Template Method inherits a skeleton — subclasses fill in steps.
4. Strategy favors composition — Template Method favors inheritance.
5. Modern Java often prefers Strategy plus lambdas over deep templates.
6. Say the force — runtime swap versus fixed sequence with customizable steps.

### Scene `teaser` (renderer: `teaser`)

1. Patterns prepared the design vocabulary — frameworks apply it at scale.
2. Episode Seventy-One — Spring Framework Intro.
3. IoC, dependency injection, and why Spring beans feel like patterns in production.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **70** — *JVM Troubleshooting*.
- **Series catalog mapping:** Episode 70 / catalog column `70` / published title *Behavioral Patterns*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Nine covered structural patterns — adapting, wrapping, and composing._
- **`title`** — starts from: _Episode Seventy._
- **`strategy`** — starts from: _Strategy defines a family of algorithms and makes them interchangeable._
- **`observer`** — starts from: _Observer notifies dependents automatically when a subject changes._
- **`command`** — starts from: _Command encapsulates a request as an object._
- **`template_iterator`** — starts from: _Template Method defines an algorithm skeleton in a base class._
- **`choose`** — starts from: _Choosing behavioral patterns in practice._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do Strategy and Template Method differ?_
- **`teaser`** — starts from: _Patterns prepared the design vocabulary — frameworks apply it at scale._
