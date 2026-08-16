# Episode 06 — Control Flow

| Field | Value |
|---|---|
| Episode | 06 |
| Title | Control Flow |
| Catalog handbook column | 6 |
| Narration source script | `make_episode_06.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Operators decide values. Control flow decides the path.
2. Which statements run? How often? When do we exit?
3. In production, unclear branching becomes missed edge cases — and messy failures.
4. Today we make the path visible — and keep it flat.

### Scene `title` (renderer: `title`)

1. Episode Six.
2. Control Flow — if, switch, loops, and clean exits.

### Scene `guards` (renderer: `guards`)

1. Start with if — but prefer guard clauses.
2. Validate early. Reject early. Return early.
3. Flat code beats a pyramid of nested else blocks.
4. If not valid — return. If not authorized — deny. Then process the happy path.
5. Readable. Testable. Kind to the next engineer.

### Scene `switch` (renderer: `switch`)

1. When cases are finite — switch shines.
2. Modern Java has switch expressions — they produce a value.
3. Arrow labels. No accidental fall-through.
4. Perfect for statuses — PENDING, PAID, CANCELLED.
5. If you are still writing classic switch with missing breaks — upgrade the habit.
6. Finite states belong in switch. Open-ended rules belong in methods.

### Scene `loops` (renderer: `loops`)

1. Loops repeat work.
2. for when you know the bounds. while when you wait on a condition.
3. for-each when you walk a collection cleanly.
4. break exits. continue skips to the next iteration.
5. Watch unbounded loops — they become production incidents.
6. And avoid allocating heavy objects on every iteration in hot paths.

### Scene `exceptions` (renderer: `exceptions`)

1. Exceptions are for exceptional paths — not everyday outcomes.
2. try, catch, finally — and try-with-resources for cleanup.
3. Open a file or connection inside try-with-resources — Java closes it for you.
4. Do not throw exceptions to mean not found on every request. That is control flow wearing a costume.
5. Reserve exceptions for failures you cannot express as a normal return.

### Scene `pipeline` (renderer: `pipeline`)

1. Picture a production request.
2. Validate. Authorize. Process. Commit. Respond.
3. On failure — compensate or retry with clear rules.
4. Good control flow makes normal and failure paths equally obvious.
5. Hidden branches are where incidents hide.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — deeply nested branches that hide the real intent.
3. Two — missing break in legacy switch — fall-through bugs.
4. Three — exceptions for common outcomes. Expensive and confusing.
5. Also — putting whole business workflows inside controllers. Extract the flow.

### Scene `interview` (renderer: `interview`)

1. Interview question — when do you use a switch expression?
2. Answer — finite, clear cases that produce a value.
3. Then add — prefer guard clauses over nesting.
4. And try-with-resources for deterministic cleanup.
5. That package of answers sounds senior.

### Scene `teaser` (renderer: `teaser`)

1. Paths are clear. Next we package behavior.
2. Episode Seven — methods.
3. Parameters, return types, overloading — how code becomes reusable.
4. See you there.

_Total beats: **47** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **6** — *Control Flow*.
- **Series catalog:** Episode 06 ↔ handbook lesson 6 — *Control Flow*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 6 excerpt)

- Control flow determines which statements execute, how often they execute, and when execution exits. Java provides
- , exceptions, and try-with-resources. Production control flow should be readable, testable, and explicit about failure paths.
- with expressions, arrow labels, pattern matching, and better exhaustiveness for modern type modeling. Try-with-resources was added to reduce resource leaks.
- Complex branching creates hidden behavior, missing edge cases, resource leaks, and hard-to-test code. In distributed systems, unclear control flow can trigger duplicate processing, missed compensation, retry storms, or swallowed failures.
- may compile to table or lookup switch bytecode. Exceptions unwind stack frames until a matching handler is found, executing
- The JVM tracks branch profiles and loop hotness. The JIT optimizes common branches, unrolls some loops, removes redundant checks, and performs deoptimization when assumptions fail. Exception paths are optimized for uncommon use, so exceptions should not contro

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 6).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Operators decide values. Control flow decides the path._
- **`title`** — starts from: _Episode Six._
- **`guards`** — starts from: _Start with if — but prefer guard clauses._
- **`switch`** — starts from: _When cases are finite — switch shines._
- **`loops`** — starts from: _Loops repeat work._
- **`exceptions`** — starts from: _Exceptions are for exceptional paths — not everyday outcomes._
- **`pipeline`** — starts from: _Picture a production request._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — when do you use a switch expression?_
- **`teaser`** — starts from: _Paths are clear. Next we package behavior._
