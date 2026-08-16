# Episode 07 — Methods

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Methods |
| Catalog handbook column | 7 |
| Narration source script | `make_episode_07.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Control flow chooses the path. Methods package the work.
2. A method is named behavior — inputs, outputs, and a contract.
3. Good method design makes APIs clear and code reusable.
4. Bad method design hides bugs inside long, unclear routines.
5. Today we learn to write methods that say what they mean.

### Scene `title` (renderer: `title`)

1. Episode Seven.
2. Methods — parameters, returns, and clean contracts.

### Scene `anatomy` (renderer: `anatomy`)

1. Look at the anatomy of a method.
2. Access modifier. Return type. Name. Parameter list.
3. Then the body — the work.
4. Name should say what it does. Parameters say what it needs.
5. Return type says what you get back — or void if it only acts.
6. Read a signature like a sentence — that is the API contract.

### Scene `signature` (renderer: `signature`)

1. The signature is the contract.
2. Same name, different parameter types — that is overloading.
3. Overloading is compile-time. The compiler picks the match.
4. Do not confuse it with overriding — that is runtime polymorphism for subclasses.
5. Keep overloads obvious. If callers guess wrong, rename.
6. Clarity beats cleverness when two methods share a name.

### Scene `design` (renderer: `design`)

1. Design tips that scale.
2. One job per method. Short enough to scan.
3. Avoid boolean flag parameters that fork behavior — split into two methods.
4. Prefer returning a clear type over returning null without a contract.
5. Domain methods beat scattered operator soup.
6. order can be cancelled is better than five comparisons copied everywhere.

### Scene `static` (renderer: `static`)

1. Instance methods need an object. Static methods do not.
2. Static helpers are fine for pure utilities.
3. But static mutable state is a trap — global lifetime, hard tests.
4. In Spring, calling this dot method may skip proxies. Know when that matters.
5. Prefer instance behavior for domain rules — static for math and parsing.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — methods that do five jobs and fill a screen.
3. Two — unclear names like process data or handle stuff.
4. Three — swallowing exceptions inside a helper so callers never learn the failure.
5. Also — making every tiny helper public. Hide what is not an API.

### Scene `interview` (renderer: `interview`)

1. Interview question — overload versus override?
2. Overload — same name, different parameters, chosen at compile time.
3. Override — subclass replaces a parent method, chosen at runtime.
4. Then add — methods should express domain intent, not just steps.
5. That answer shows you design APIs, not just syntax.

### Scene `teaser` (renderer: `teaser`)

1. Behavior is packaged. Next we hold many values.
2. Episode Eight — arrays.
3. Fixed size, indexed access, and the off-by-one traps.
4. See you there.

_Total beats: **44** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **7** — *Methods*.
- **Series catalog:** Episode 07 ↔ handbook lesson 7 — *Methods*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 7 excerpt)

- Concept: Methods define named behavior with inputs, outputs, side effects, contracts, and visibility. In senior-level Java, method design controls API clarity, testability, transaction boundaries, latency, coupling, and domain expressiveness.
- Mistakes: Common mistakes include long methods, unclear names, boolean parameter traps, returning null without contract, swallowing exceptions, mixing I/O and domain rules, self-invoking proxied Spring methods, and making every helper public.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 7).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Control flow chooses the path. Methods package the work._
- **`title`** — starts from: _Episode Seven._
- **`anatomy`** — starts from: _Look at the anatomy of a method._
- **`signature`** — starts from: _The signature is the contract._
- **`design`** — starts from: _Design tips that scale._
- **`static`** — starts from: _Instance methods need an object. Static methods do not._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — overload versus override?_
- **`teaser`** — starts from: _Behavior is packaged. Next we hold many values._
