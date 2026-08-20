# Episode 10 — Object-Oriented Programming

| Field | Value |
|---|---|
| Episode | 10 |
| Title | Object-Oriented Programming |
| Catalog handbook column | 10 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Strings and arrays hold data. Objects model the world.
2. State, behavior, identity — working together.
3. OOP in Java is how teams manage domain complexity — not just a syntax style.
4. Classes are blueprints. Objects are living instances on the heap.

### Scene `title` (renderer: `title`)

1. Episode Ten.
2. Object-Oriented Programming — classes, objects, and encapsulation.

### Scene `class_obj` (renderer: `class_obj`)

1. Class — blueprint. Fields hold state. Methods hold behavior.
2. new BankAccount creates an object — unique identity.
3. Two objects same class — different instances, different identity.
4. == compares identity for objects. equals compares value when overridden.

### Scene `encaps` (renderer: `encaps`)

1. Encapsulation — hide internals, expose intention.
2. private fields. public methods enforcing invariants.
3. Callers should not set balanceInCents directly if rules apply.
4. Methods like deposit express domain language.
5. Encapsulation is protection — not ceremony.

### Scene `example` (renderer: `example`)

1. Walk a small account type.
```java
public class BankAccount {
    private final String id;
    private long balanceInCents;

    public BankAccount(String id, long openingBalance) {
        this.id = id;
        this.balanceInCents = openingBalance;
    }

    public void deposit(long cents) {
        if (cents <= 0) throw new IllegalArgumentException("positive deposit only");
        balanceInCents += cents;
    }

    public long balanceInCents() {
        return balanceInCents;
    }
}
```

2. private fields — state hidden.
3. Constructor sets initial state.
4. deposit validates positive amount — invariant enforced at boundary.
5. balanceInCents accessor — read without exposing mutation path.

### Scene `pillars` (renderer: `pillars`)

1. Four pillars people cite.
2. Encapsulation — hide details.
3. Abstraction — show what matters.
4. Inheritance — share and specialize — carefully.
5. Polymorphism — one interface, many implementations.
6. Prefer composition — has-a — when inheritance trees get deep.

### Scene `compose` (renderer: `compose`)

1. Composition — Order has Money, Customer has Address.
2. Small collaborating objects beat god classes.
3. Anemic model — data only in entities, all logic in services — loses clarity.
4. Put behavior next to data it protects.

### Scene `deeper` (renderer: `deeper`)

1. this reference — current object inside instance methods.
2. super — call superclass constructor or method — must be first in constructor if used.
3. Constructor chaining — this(...) or super(...) — one must be first statement.
4. Default constructor inserted if none written — only if no other constructors.
5. Initialization order — static fields, static blocks, instance fields, instance blocks, constructor.
6. Wrong order assumptions cause subtle null bugs with overridden methods in constructors.
7. Interfaces define contracts — multiple interfaces on one class — no multiple inheritance of state.
8. Abstract classes — mix abstract and concrete methods — share code with partial implementation.
9. final class cannot be extended — String is final — security and immutability.
10. final methods cannot be overridden — rare in application code.
11. Object methods — equals, hashCode, toString — override together with consistent contract.

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
2. One — god services doing every use case.
3. Two — deep fragile inheritance.
4. Three — public mutable fields.
5. Leaking JPA entities through REST APIs — coupling nightmare.

### Scene `interview` (renderer: `interview`)

1. Interview — class versus object?
2. Class blueprint. Object instance with identity and state.
3. Encapsulation — hide fields, expose behavior.
4. Composition over deep inheritance.

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

### Scene `polymorphism` (renderer: `polymorphism`)

1. Reference type PaymentProcessor — instance CreditCardProcessor or PayPalProcessor.
2. Virtual method dispatch — JVM calls runtime type's override — core polymorphism.
3. Upcasting to interface — List list = new ArrayList — lose concrete API unless cast.
4. Downcast only when sure — instanceof guard first — ClassCastException otherwise.

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

### Scene `summary` (renderer: `summary`)

1. OOP models collaborating objects.
2. Encapsulate state. Express domain in methods.
3. Composition often beats inheritance depth.
4. Identity and equality are distinct concepts.
5. Design for change at object boundaries.

### Scene `teaser` (renderer: `teaser`)

1. Objects need boundaries. Next — who can see what.
2. Episode Eleven — Access Modifiers.
3. private, public, protected, package-private.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **10** — *Object-Oriented Programming*.
- **Series catalog:** Episode 10 ↔ handbook lesson 10 — *Object-Oriented Programming*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 10 excerpt)

- Concept: Object-oriented programming models software as collaborating objects with state, behavior, identity, and contracts. In Java, OOP includes classes, interfaces, encapsulation, inheritance, polymorphism, composition, and abstraction. For architects, OOP 
- Mistakes: Common mistakes include anemic domain models, god services, deep inheritance trees, public mutable fields, interfaces without purpose, leaking persistence entities through APIs, and confusing Java interfaces with distrib

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 10).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Strings and arrays hold data. Objects model the world._
- **`title`** — starts from: _Episode Ten._
- **`class_obj`** — starts from: _A class is the blueprint._
- **`encaps`** — starts from: _Encapsulation hides internals behind a clear API._
- **`pillars`** — starts from: _Four ideas you will hear forever._
- **`compose`** — starts from: _Composition says has-a._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — class versus object?_
- **`teaser`** — starts from: _Objects need boundaries. Next — who can see what._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
