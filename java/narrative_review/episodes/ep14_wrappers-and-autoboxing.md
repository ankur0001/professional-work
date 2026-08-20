# Episode 14 — Wrappers and Autoboxing

| Field | Value |
|---|---|
| Episode | 14 |
| Title | Wrappers and Autoboxing |
| Catalog handbook column | 14 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Enums gave type-safe states. Now numbers as objects.
2. int primitive. Integer wrapper — nullable object.
3. Autoboxing hides conversion — and hides costs and crashes.
4. Collections need objects — wrappers bridge the gap.

### Scene `title` (renderer: `title`)

1. Episode Fourteen.
2. Wrappers and Autoboxing — objects around primitives.

### Scene `pairs` (renderer: `pairs`)

1. Eight primitives. Eight wrappers.
2. Wrappers on heap — identity, null allowed.
3. Default to primitives unless nullability required.

### Scene `autobox` (renderer: `autobox`)

1. Integer x = 10 boxes int.
2. int y = x unboxes.
3. Null Integer unboxed — NullPointerException.
4. Silent conversion plus null is production trap.

### Scene `example` (renderer: `example`)

1. Walk list of integers.
```java
import java.util.ArrayList;
import java.util.List;

public class WrapperDemo {
    public static void main(String[] args) {
        int primitive = 42;
        Integer boxed = primitive;       // autobox
        int unboxed = boxed;             // unbox

        List<Integer> counts = new ArrayList<>();
        counts.add(10);                  // autobox on add
        int first = counts.get(0);       // unbox on read
    }
}
```

2. counts.add(10) autoboxes.
3. get(0) unboxes to int.
4. Hot loops through boxed lists allocate heavily.

### Scene `cost` (renderer: `cost`)

1. Object header and indirection versus raw int.
2. List<Integer> versus int[] in hot numeric code.
3. Measure before boxing every number.

### Scene `cache` (renderer: `cache`)

1. Integer caches small values — == may appear to work.
2. Always use equals for wrapper comparison.

### Scene `deeper` (renderer: `deeper`)

1. ValueOf and parse methods on wrappers — prefer over constructors — caching.
2. Boolean.TRUE and FALSE instances — use instead of new Boolean.
3. OptionalInt, OptionalLong, OptionalDouble — avoid boxing in streams — performance.
4. Primitive streams — IntStream, LongStream — specialized operations without boxing.
5. Null in Map of Integer — HashMap allows null key once — know your map implementation.
6. Concurrent collections — never null keys or values on ConcurrentHashMap.
7. Performance test — boxing one million integers — measurable GC — profile before optimizing.

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

1. Unboxing null.
2. Wrappers in hot loops without need.
3. == on wrappers.
4. Nullable Boolean in conditions without null check.

### Scene `interview` (renderer: `interview`)

1. Primitive versus wrapper — value, null, overhead, autoboxing NPE.

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

### Scene `revision` (renderer: `revision`)

1. Quick revision beat — say the definition out loud without looking.
2. Explain it to an imaginary junior on your team in two sentences.
3. Name one production mistake this feature prevents when used correctly.
4. Name one mistake it causes when used incorrectly.
5. Connect to interview — one question, one crisp answer — practice now.
6. If you cannot explain it simply, revisit the example scene once more.
7. Solid Phase One fundamentals make Phase Two collections feel easy instead of magical.

### Scene `deep_dive` (renderer: `deep_dive`)

1. Deep dive moment — watch this carefully.
2. In a code review, ask: does this code teach the reader the domain rule?
3. Tests should document edge cases — null, empty, boundary, overflow where relevant.
4. Logging — log identifiers and outcomes, not secrets — strings appear in logs constantly.
5. Metrics — count failures of this operation — helps SRE spot regressions after deploy.
6. Feature flags — control flow at deploy time — still write clear Java structure underneath.
7. Refactoring — rename for intent before optimizing — clarity first, microseconds second.
8. Pair with the handbook revision sheet — twenty bullets beat rereading eighty pages blindly.
9. OpenJDK documentation and Javadoc — authoritative when interview answers need precision.
10. Stack Overflow answers vary in quality — verify against language spec for edge cases.
11. Your future self maintains this code — write the explanation you wish you had today.
12. Teaching solid Java fundamentals reduces incident pages on-call — that is the real ROI.

### Scene `floor` (renderer: `floor`)

1. Before we wrap — one more real-world tie-in.
2. Teams that document these choices in ADRs avoid re-debating them every sprint.
3. Onboarding docs linking to this episode save senior engineers from repeating the same lecture.
4. Lint rules and static analysis encode some of this — SpotBugs, Error Prone, Checkstyle — pick your stack.
5. Consistency across microservices matters — shared library for Money type beats ten incompatible doubles.

### Scene `summary` (renderer: `summary`)

1. Wrappers enable null and collections.
2. Autoboxing convenient — not free.
3. Prefer primitives in hot paths.

### Scene `teaser` (renderer: `teaser`)

1. Objects around values. Next — type-safe containers.
2. Episode Fifteen — Generics.
3. List of Order without casts.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **14** — *Wrappers and Autoboxing*.
- **Series catalog:** Episode 14 ↔ handbook lesson 14 — *Wrappers and Autoboxing*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Enums gave us type-safe states. Now look at numbers as objects._
- **`title`** — starts from: _Episode Fourteen._
- **`pairs`** — starts from: _Eight primitives. Eight wrappers._
- **`autobox`** — starts from: _Autoboxing converts automatically._
- **`cost`** — starts from: _Wrappers cost more than primitives._
- **`cache`** — starts from: _One more quirk — Integer caching._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — primitive versus wrapper?_
- **`teaser`** — starts from: _Objects around values. Next — type-safe containers._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
