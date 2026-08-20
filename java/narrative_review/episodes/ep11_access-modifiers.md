# Episode 11 — Access Modifiers

| Field | Value |
|---|---|
| Episode | 11 |
| Title | Access Modifiers |
| Catalog handbook column | 11 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Objects need boundaries. Access modifiers draw the lines.
2. Who sees this field? Who calls this method?
3. Visibility is ownership encoded in syntax.
4. Not an afterthought — an architecture decision in miniature.

### Scene `title` (renderer: `title`)

1. Episode Eleven.
2. Access Modifiers — private, public, protected, package-private.

### Scene `levels` (renderer: `levels`)

1. Four levels — narrow to wide.
2. private — declaring class only.
3. package-private — no modifier — same package.
4. protected — package plus subclasses.
5. public — everyone. A promise.
6. Default to narrowest that works. Widen with intent.

### Scene `private` (renderer: `private`)

1. private first — fields and helpers.
2. If everything is public — no boundary, only hope.
3. Tests can use package-private collaborators in same package test sources.

### Scene `package` (renderer: `package`)

1. Package-private underrated.
2. Internal collaboration without publishing API.
3. Accidental public grows compatibility obligations forever.

### Scene `example` (renderer: `example`)

1. Walk facade hiding calculator.
```java
public class InvoiceFacade {
    private final TaxCalculator calculator = new TaxCalculator();

    public Money totalWithTax(Money subtotal) {
        return calculator.applyTax(subtotal);
    }
}

class TaxCalculator {
    Money applyTax(Money subtotal) {
        return subtotal; // package-private collaborator
    }
}
```

2. InvoiceFacade public — stable entry.
3. TaxCalculator package-private — internal to billing package.
4. Only facade crosses package boundary in public API.

### Scene `protected_public` (renderer: `protected_public`)

1. protected for extension points in inheritance hierarchies.
2. public is published contract — every method maintained across releases.
3. Libraries minimize public surface. Applications too.

### Scene `deeper` (renderer: `deeper`)

1. Top-level classes — only public or package-private.
2. Nested classes — static nested, inner, local, anonymous — different visibility and this binding.
3. Inner class holds implicit reference to outer — memory leak risk if outer outlives needed scope.
4. Static nested class — no outer reference — prefer when nesting is organizational.
5. Module system adds another layer — exports and opens — Episode Twenty.
6. public on interface methods is implicit — redundant but readable.
7. Sealed types restrict who extends — Episode Nineteen — interacts with protected visibility.
8. Library design — minimize public, document package-private collaborators in module docs.
9. JPMS exports package — access modifiers still apply inside module.

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
2. One — public fields.
3. Two — public everything just in case.
4. Three — widening visibility to fix tests instead of redesign.

### Scene `interview` (renderer: `interview`)

1. Interview — default versus private?
2. Default package-private — same package sees it.
3. private — declaring class only.
4. Prefer narrowest visibility. public is contract.

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

### Scene `summary` (renderer: `summary`)

1. Access modifiers encode ownership.
2. Start private. Use package for internal neighbors.
3. public is long-term promise.
4. Visibility shapes API evolution and test design.

### Scene `teaser` (renderer: `teaser`)

1. Visibility needs a home. Next — packages.
2. Episode Twelve — Packages.
3. Namespaces, boundaries, ownership on disk.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **11** — *Access Modifiers*.
- **Series catalog:** Episode 11 ↔ handbook lesson 11 — *Access Modifiers*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 11 excerpt)

- Concept: Access modifiers define visibility boundaries for classes, constructors, fields, and methods. Java uses them to encode ownership: private for implementation detail, package-private for module-internal collaboration, protected for inheritance-aware ext

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 11).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Objects need boundaries. Access modifiers draw those lines._
- **`title`** — starts from: _Episode Eleven._
- **`levels`** — starts from: _Four levels. Narrow to wide._
- **`private`** — starts from: _private is your first encapsulation tool._
- **`package`** — starts from: _Package-private is underrated._
- **`protected_public`** — starts from: _protected supports inheritance-aware extension._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — default access versus private?_
- **`teaser`** — starts from: _Visibility needs a home. Next — packages._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
