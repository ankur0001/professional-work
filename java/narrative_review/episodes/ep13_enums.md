# Episode 13 — Enums

| Field | Value |
|---|---|
| Episode | 13 |
| Title | Enums |
| Catalog handbook column | 13 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Packages organize types. Enums organize fixed choices.
2. PENDING, PAID, CANCELLED — not free-form strings drifting across services.
3. Type-safe constants with behavior attached.
4. Replace magic strings with domain vocabulary the compiler knows.

### Scene `title` (renderer: `title`)

1. Episode Thirteen.
2. Enums — type-safe states instead of magic strings.

### Scene `basics` (renderer: `basics`)

1. enum OrderStatus — each constant is singleton instance.
2. Compare with == safely — identity stable.
3. Switch expressions love enums — finite exhaustive cases.
4. Compiler helps when you add a new constant — update switches.

### Scene `behavior` (renderer: `behavior`)

1. Enums can have fields, constructors, methods.
2. Attach labels and transition rules next to constants.
3. Better than String.equals scattered in five services.

### Scene `example` (renderer: `example`)

1. Walk status enum with transitions.
```java
public enum OrderStatus {
    PENDING("Awaiting payment"),
    PAID("Ready to ship"),
    SHIPPED("In transit"),
    CANCELLED("Closed");

    private final String label;
    OrderStatus(String label) { this.label = label; }

    public String label() { return label; }

    public boolean canTransitionTo(OrderStatus next) {
        return switch (this) {
            case PENDING -> next == PAID || next == CANCELLED;
            case PAID -> next == SHIPPED;
            default -> false;
        };
    }
}
```

2. Each constant calls constructor with display label.
3. canTransitionTo encodes allowed moves — domain rule on the type.
4. Switch on enum elsewhere stays readable and finite.

### Scene `vs_string` (renderer: `vs_string`)

1. String status = PAID — typos compile. Invalid states sneak in.
2. Enums reject invalid assignments at compile time.
3. Persistence — prefer name over ordinal. Ordinal reorder breaks databases.

### Scene `enumset` (renderer: `enumset`)

1. EnumSet for enum flag combinations — fast and compact.
2. Better than raw int bitmasks unless you truly need bits.

### Scene `deeper` (renderer: `deeper`)

1. Enum implements Comparable — natural order is declaration order.
2. values() and valueOf — parse from string name — IllegalArgumentException if unknown.
3. Custom constructor on enum must be private — compiler enforces.
4. Enum singleton pattern — effective single instance — Joshua Bloch recommended.
5. Switch on enum — compiler knows all constants — add constant, fix switches.
6. Serialization — readResolve can protect singleton enums — built-in protection.
7. GraphQL and OpenAPI enums — name strings must match API contract — document mapping.

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
2. Stringly typed statuses.
3. ordinal in database columns.
4. Enums for volatile business catalogs that change weekly.

### Scene `interview` (renderer: `interview`)

1. Interview — enums versus strings?
2. Type safety. Exhaustive switches. Behavior on constants.
3. Persist name not ordinal.

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

1. Enums model fixed vocabularies.
2. Constants are objects — can carry logic.
3. Prefer over magic strings for states and categories.

### Scene `teaser` (renderer: `teaser`)

1. Fixed states clear. Next — primitives as objects.
2. Episode Fourteen — Wrappers and Autoboxing.
3. Integer, nullability, hidden allocations.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **13** — *Enums*.
- **Series catalog:** Episode 13 ↔ handbook lesson 13 — *Enums*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Packages organize types. Enums organize fixed choices._
- **`title`** — starts from: _Episode Thirteen._
- **`basics`** — starts from: _Declare an enum like a special class._
- **`behavior`** — starts from: _Enums can carry fields and methods._
- **`vs_string`** — starts from: _Why not String status equals PAID?_
- **`enumset`** — starts from: _Need a set of flags? EnumSet is built for enums._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why prefer enums over string constants?_
- **`teaser`** — starts from: _Fixed states are clear. Next — when primitives become objects._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
