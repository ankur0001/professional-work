# Episode 07 — Methods

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Methods |
| Catalog handbook column | 7 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Control flow chooses the path. Methods package the work.
2. A method is named behavior — inputs, outputs, side effects, visibility.
3. Good methods make APIs clear. Bad methods hide bugs in long routines.
4. Senior Java is mostly method design — domain language at the right boundaries.

### Scene `title` (renderer: `title`)

1. Episode Seven.
2. Methods — parameters, returns, and clean contracts.

### Scene `anatomy` (renderer: `anatomy`)

1. Anatomy of a method.
2. Access modifier. Return type. Name. Parameter list. Body.
3. Name says what it does. Parameters say what it needs.
4. Return type says what you get — void if it only acts.
5. Read a signature like a sentence — that is the contract callers depend on.

### Scene `signature` (renderer: `signature`)

1. The signature is the contract.
2. Same name, different parameter types — overloading. Compiler picks at compile time.
3. Override — subclass replaces parent method — runtime polymorphism. Different idea.
4. Keep overloads obvious. If callers guess wrong, rename instead.
5. Varargs — String... parts — sparingly. Lists often clearer.

### Scene `example` (renderer: `example`)

1. Walk domain methods on an order service.
```java
public class OrderService {
    public boolean canBeCancelled(Order order) {
        return order.status() == OrderStatus.PENDING;
    }

    public void cancel(Order order) {
        if (!canBeCancelled(order)) {
            throw new IllegalStateException("cannot cancel");
        }
        order.markCancelled();
    }

    public static int compareByAmount(Order a, Order b) {
        return Long.compare(a.amountInCents(), b.amountInCents());
    }
}
```

2. canBeCancelled encodes a rule — better than five comparisons copied in controllers.
3. cancel validates then mutates — guard clause inside method.
4. compareByAmount static — utility on type, no instance needed.
5. Methods should express domain intent — not just mechanical steps.

### Scene `design` (renderer: `design`)

1. Design tips that scale.
2. One job per method. Short enough to scan in a code review.
3. Avoid boolean flag parameters that fork behavior — split into two methods.
4. Prefer clear return types over returning null without contract — Optional later in Episode Thirty.
5. Do not swallow exceptions in helpers — callers need failure signals.
6. Hide helpers as private unless they are real API.

### Scene `static` (renderer: `static`)

1. Instance methods need an object. Static methods belong to the class.
2. Static utilities fine for pure functions — parsing, math.
3. Static mutable state is global — concurrency and test pollution.
4. In Spring, this.method() from same class may skip transactional proxy — know AOP boundaries.
5. Prefer instance behavior for domain rules.

### Scene `deeper` (renderer: `deeper`)

1. Parameters are pass-by-value — always.
2. For references, the reference value is copied — both point at same object.
3. Reassigning parameter to new object does not affect caller's variable.
4. Mutating object through reference is visible to caller — know the difference.
5. Varargs — public void log(String level, String... messages) — treat as array inside.
6. Overloading resolution picks most specific match — ambiguity compile error.
7. Bridge methods and generics — rare interview topic — compiler synthesizes bridges for erasure.
8. Recursion has stack depth limits — deep recursion risks StackOverflowError.
9. Tail recursion is not optimized by standard HotSpot — use loops for deep iteration.
10. Method references — System.out::println — shorthand for lambdas, Episode Twenty-Six area.

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
2. One — screen-long methods doing five jobs.
3. Two — names like processData or handleStuff.
4. Three — swallowing exceptions so callers never learn failure.
5. Also — every helper public — no encapsulation left.

### Scene `interview` (renderer: `interview`)

1. Interview — overload versus override?
2. Overload — same name, different parameters, compile time.
3. Override — subclass replaces inherited method, runtime dispatch.
4. Methods should express domain intent.
5. Boolean flag parameters are a design smell — split methods.

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

### Scene `contracts` (renderer: `contracts`)

1. Preconditions — validate arguments at method entry — fail fast IllegalArgumentException.
2. Postconditions — guarantee on return — document in javadoc or tests.
3. JavaDoc @param @return @throws — contract for public API.
4. Defensive copy on getters for mutable internal state — return List.copyOf.
5. Fail fast versus fail safe — domain methods usually fail fast on invalid input.

### Scene `summary` (renderer: `summary`)

1. Methods package behavior with contracts.
2. Signatures are API promises. Overload carefully. Override for polymorphism.
3. Domain methods beat scattered operator soup.
4. Static for utilities — not mutable global state.
5. Name and size methods for the reader who arrives at three a.m.

### Scene `teaser` (renderer: `teaser`)

1. Behavior is packaged. Next — hold many values.
2. Episode Eight — Arrays.
3. Fixed size, indexed access, off-by-one traps.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **7** — *Methods*.
- **Series catalog:** Episode 07 ↔ handbook lesson 7 — *Methods*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

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

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
