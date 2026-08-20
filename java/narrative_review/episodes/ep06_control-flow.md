# Episode 06 — Control Flow

| Field | Value |
|---|---|
| Episode | 06 |
| Title | Control Flow |
| Catalog handbook column | 6 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Operators decide values. Control flow decides which statements run.
2. Which path executes? How often? When do we exit?
3. In production, unclear branching becomes missed edge cases and messy failures.
4. Distributed systems amplify bad flow — duplicate processing, retry storms, swallowed errors.
5. Today we make paths visible — flat, explicit, testable.

### Scene `title` (renderer: `title`)

1. Episode Six.
2. Control Flow — if, switch, loops, and clean exits.

### Scene `guards` (renderer: `guards`)

1. Start with if — but prefer guard clauses.
2. Validate early. Reject early. Return early.
3. Flat code beats a pyramid of nested else blocks.
4. if not valid — return bad request. if not authorized — return forbidden.
5. Then process the happy path at low indentation.
6. Readable. Testable. Kind to the next engineer at three a.m.

### Scene `switch` (renderer: `switch`)

1. When cases are finite — switch shines.
2. Modern switch expressions produce a value — arrow labels, no fall-through.
3. Perfect for statuses — PENDING, PAID, CANCELLED, SHIPPED.
4. Classic switch without break caused decades of bugs — upgrade the habit.
5. Pattern matching plus sealed types later make switches exhaustive — Episodes Eighteen and Nineteen.
6. Finite states belong in switch. Open-ended rules belong in methods.

### Scene `loops` (renderer: `loops`)

1. Loops repeat work.
2. for when you know bounds. while when waiting on a condition.
3. Enhanced for-each when walking collections cleanly.
4. break exits. continue skips to next iteration.
5. Unbounded loops become incidents. Off-by-one loops become ArrayIndexOutOfBounds.
6. Avoid heavy allocation every iteration in hot paths.

### Scene `example` (renderer: `example`)

1. Walk a switch expression routing order status.
```java
public enum OrderStatus { PENDING, PAID, CANCELLED, SHIPPED }

public class OrderRouter {
    static String nextAction(OrderStatus status) {
        return switch (status) {
            case PENDING -> "await_payment";
            case PAID -> "fulfill";
            case CANCELLED -> "archive";
            case SHIPPED -> "track";
        };
    }
}
```

2. OrderStatus enum — finite set of states.
3. switch expression returns a String action — each case an arrow label.
4. Compiler checks exhaustiveness when all enum constants covered.
5. No break needed — arrow form does not fall through.
6. This is readable control flow — status to action in one place.

### Scene `exceptions` (renderer: `exceptions`)

1. Exceptions are for exceptional paths — not everyday outcomes.
2. try, catch, finally — and try-with-resources for deterministic cleanup.
3. Open JDBC connection or InputStream in try-with-resources — close called automatically.
4. Do not throw exceptions to mean not found on every request — that is expensive control flow.
5. Reserve exceptions for failures you cannot express as a normal return.
6. Episode Thirty-Two goes deep on exception design — today know the boundary.

### Scene `pipeline` (renderer: `pipeline`)

1. Picture a production request pipeline.
2. Validate. Authorize. Process. Commit. Respond.
3. On failure — compensate or retry with idempotency keys and clear rules.
4. Good flow makes normal and failure paths equally obvious.
5. Hidden branches are where incidents hide — log and test both paths.

### Scene `deeper` (renderer: `deeper`)

1. do-while runs body at least once — rare but useful for retry prompts.
2. Labeled break and continue exist — avoid unless clarifying nested loops.
3. Pattern matching in switch — switch (obj) { case String s -> ... } — Java 21+ style.
4. Combines type check and binding — pairs with sealed types later.
5. Yield in switch blocks when arrow form needs multiple statements.
6. InterruptedException in loops — restore interrupt flag or exit cleanly.
7. Ignoring Thread.interrupted() causes shutdown hooks and pool stops to hang.
8. Finally runs even when return in try — mind return values overwritten by finally return.
9. Try-with-resources can suppress secondary exceptions from close — suppressed array on primary.

### Scene `production` (renderer: `production`)

1. Production context — why this topic stops incidents.
2. Code review checklist item — catch misuse before merge.
3. Observability — logs and metrics should name concepts clearly — not mystery abbreviations.
4. Tests should encode the contracts we discussed — one failing test beats ten slides.
5. Refactor toward clarity — juniors read this code six months from now.
6. Interview answers map directly to daily choices — not trivia for trivia's sake.
7. Connect to handbook lesson themes — JVM, structure, types, concurrency later in series.
8. Next episodes build on this — skipping fundamentals creates gaps that show in system design.

### Scene `mistakes` (renderer: `mistakes`)

1. Three mistakes.
2. One — deeply nested branches hiding intent.
3. Two — missing break in legacy switch — fall-through bugs.
4. Three — exceptions for common outcomes.
5. Also — entire business workflows stuffed in controllers — extract services.

### Scene `interview` (renderer: `interview`)

1. Interview — when use switch expression?
2. Finite, clear cases that produce a value.
3. Prefer guard clauses over nesting.
4. try-with-resources for deterministic cleanup.
5. Do not use exceptions for normal control flow — cost and clarity.
6. That package sounds senior.

### Scene `walkthrough2` (renderer: `walkthrough2`)

1. Let's slow down once more with a reviewer mindset.
2. If you saw this in a pull request, what would you comment?
3. Naming clarity, null safety, visibility, performance — rotate through that checklist.
4. Let me say that again in plain language — because this is the kind of detail interviews probe and production punishes.
5. When you read open-source Java or a teammate's pull request, you'll recognize these patterns immediately.
6. Pause the video if you want — write a five-line example in your scratch project. Muscle memory beats passive watching.
7. The handbook treats this as foundational for eighty lessons — JVM tuning, Spring, concurrency all assume you know this cold.
8. We're not racing the syllabus. We're building mental models that survive version upgrades and job changes.
9. Senior engineers don't know every API by heart. They know where to look and which mistakes repeat.
10. Junior engineers who nail fundamentals ramp faster on frameworks — Spring, JPA, Kafka all sit on this base.
11. Your IDE helps — but only after you understand what the compiler and JVM will accept and reject.
12. Compile errors are friends. They prevent runtime surprises in customer environments.
13. Runtime errors with stack traces — read bottom up to your code first, then framework frames.
14. Unit tests for this topic should be small — one concept per test method — not thousand-line integration only.
15. When stuck, reduce to main in a scratch class — isolate the language feature from framework noise.

### Scene `connect` (renderer: `connect`)

1. Connect backward — Episode One gave portability. Episode Two named the toolchain.
2. Connect forward — collections, streams, and concurrency assume today's concept is solid.
3. The Java Story is cumulative — skipping an episode creates a hole you feel later as confusion.
4. Bookmark the handbook lesson that matches this episode — revision sheet before interviews.
5. Production stories in later episodes reference types and structures we defined in Phase One.
6. You are still in Phase One — language and platform — the bedrock everything else stands on.
7. Architects who skipped fundamentals design APIs that leak abstraction — don't skip.
8. Teaching this to a teammate? Use the same order — hook, example, mistake, interview answer.
9. Documentation you write for your team should mirror these boundaries — package, type, method.
10. Code is read more than written — optimize for the reader who has no context yet.

### Scene `workflow` (renderer: `workflow`)

1. State machines — enum status plus switch — cleaner than string state scattered.
2. Idempotency keys in HTTP handlers — control flow for retries — same request safe twice.
3. Circuit breaker — if failures exceed threshold — short-circuit further calls — control flow at system level.
4. Saga compensation — if step three fails — run undo for step two — explicit failure graph.

### Scene `summary` (renderer: `summary`)

1. Control flow shapes reliability.
2. Guard clauses flatten code. Switch handles finite states.
3. Loops need bounds and allocation discipline.
4. Exceptions for failures — not regular branches.
5. Make failure paths as visible as happy paths.

### Scene `teaser` (renderer: `teaser`)

1. Paths are clear. Next — package behavior.
2. Episode Seven — Methods.
3. Parameters, returns, overloading — reusable named work.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **6** — *Control Flow*.
- **Series catalog:** Episode 06 ↔ handbook lesson 6 — *Control Flow*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

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

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
