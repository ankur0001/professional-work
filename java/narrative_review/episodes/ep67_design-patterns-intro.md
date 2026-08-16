# Episode 67 — Design Patterns Intro

| Field | Value |
|---|---|
| Episode | 67 |
| Title | Design Patterns Intro |
| Catalog handbook column | 67 |
| Narration source script | `make_episode_67.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Six wrapped JVM interview answers — heap, GC, JIT, and measurement.
2. Architecture interviews shift next — from how the JVM runs code to how you structure code.
3. Design patterns are reusable solutions to recurring software design problems.
4. They are not libraries — they are named ideas teams use to communicate intent.
5. Junior engineers memorize names — seniors know when a pattern helps and when it hurts.
6. Today — what patterns are, the three GoF categories, and how Java already uses them.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Seven.
2. Design Patterns Intro.

### Scene `what_patterns` (renderer: `what_patterns`)

1. A design pattern names a proven structure for a common problem.
2. The Gang of Four book cataloged twenty-three classic object-oriented patterns.
3. Each pattern has a problem, a structure, consequences, and known uses.
4. Patterns create a shared vocabulary — say Adapter and teammates know the shape.
5. They are tools for clarity — not badges to sprinkle on every class.
6. Prefer the simplest design that communicates intent — patterns when complexity earns them.

### Scene `three_categories` (renderer: `three_categories`)

1. Patterns group into three categories by intent.
2. Creational — control how objects are created — Singleton, Factory, Builder.
3. Structural — compose classes and objects — Adapter, Decorator, Facade, Proxy.
4. Behavioral — organize communication and algorithms — Strategy, Observer, Command.
5. Episodes Sixty-Eight through Seventy walk each category with Java examples.
6. Category first — then pick the pattern that matches the force you are balancing.

### Scene `java_already` (renderer: `java_already`)

1. Java's standard library is full of patterns you already use.
2. Iterator — for-each loops walk collections without exposing structure.
3. Observer — listeners and reactive streams notify interested parties.
4. Decorator — java.io streams wrap streams — BufferedInputStream over FileInputStream.
5. Factory — Calendar.getInstance and Paths.get hide concrete construction.
6. Recognizing patterns in the JDK trains your eye for application design.

### Scene `when_to_use` (renderer: `when_to_use`)

1. Use a pattern when the problem matches — not when you want a fancy name.
2. Duplicated construction logic — consider Factory or Builder.
3. Need to swap algorithms at runtime — Strategy fits cleanly.
4. Legacy API mismatch — Adapter bridges without rewriting callers.
5. If a pattern adds classes without reducing coupling — skip it.
6. Readability for your team beats purity from a textbook.

### Scene `anti_patterns` (renderer: `anti_patterns`)

1. Pattern abuse is a real failure mode.
2. Singleton everywhere — hidden global state that breaks tests.
3. Abstract factory for two concrete types — ceremony without payoff.
4. Observer graphs so tangled that change ripples unpredictably.
5. Also — renaming a simple method call a Strategy without a family of algorithms.
6. Patterns serve design — design does not serve pattern checklists.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — memorizing twenty-three names without a problem they solve.
3. Two — forcing patterns into code that is already clear.
4. Three — confusing design patterns with architectural styles like microservices.
5. Also — skipping trade-offs — every pattern adds indirection cost.
6. Name the force, then the pattern — never the reverse.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is a design pattern and why use one?
2. A named, reusable solution to a recurring design problem.
3. It improves communication — teams share intent with one word.
4. It packages trade-offs — you adopt known consequences deliberately.
5. Java's JDK uses patterns heavily — Iterator, Decorator, Factory.
6. Use them when they reduce coupling or clarify variation — not for prestige.

### Scene `teaser` (renderer: `teaser`)

1. Next we go deep on object creation.
2. Episode Sixty-Eight — Creational Patterns.
3. Singleton, Factory Method, Abstract Factory, Builder, and Prototype.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **67** — *ZGC & Shenandoah*.
- **Series catalog mapping:** Episode 67 / catalog column `67` / published title *Design Patterns Intro*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Six wrapped JVM interview answers — heap, GC, JIT, and measurement._
- **`title`** — starts from: _Episode Sixty-Seven._
- **`what_patterns`** — starts from: _A design pattern names a proven structure for a common problem._
- **`three_categories`** — starts from: _Patterns group into three categories by intent._
- **`java_already`** — starts from: _Java's standard library is full of patterns you already use._
- **`when_to_use`** — starts from: _Use a pattern when the problem matches — not when you want a fancy name._
- **`anti_patterns`** — starts from: _Pattern abuse is a real failure mode._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is a design pattern and why use one?_
- **`teaser`** — starts from: _Next we go deep on object creation._
