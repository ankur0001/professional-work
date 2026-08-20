# Episode 12 — Packages

| Field | Value |
|---|---|
| Episode | 12 |
| Title | Packages |
| Catalog handbook column | 12 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Access needs neighborhoods. Packages are those neighborhoods.
2. Namespace and boundary — on disk and at runtime.
3. Prevent name collisions. Shape collaboration.
4. Folder tree should tell the truth about ownership.

### Scene `title` (renderer: `title`)

1. Episode Twelve.
2. Packages — namespaces, boundaries, and ownership.

### Scene `namespace` (renderer: `namespace`)

1. package com.acme.orders.domain — part of binary class name.
2. com.acme.OrderService distinct from com.other.OrderService.
3. Directory path must match package declaration.
4. Break mapping — IDE and compiler angry.

### Scene `boundary` (renderer: `boundary`)

1. Package-private visibility scoped to package.
2. External code uses public API types only.
3. Good packages make illegal dependencies awkward.
4. One giant util package erases boundaries.

### Scene `structure` (renderer: `structure`)

1. Organize by capability — api, application, domain, infrastructure.
2. Or by feature when teams own features end to end.
3. Pure layers alone can become anemic and tangled.
4. Pick structure matching ownership and dependency direction.

### Scene `example` (renderer: `example`)

1. Walk application root placement.
```java
package com.acme.orders;

import com.acme.orders.domain.Order;
import com.acme.orders.api.OrderController;

public class OrdersApplication {
    public static void main(String[] args) {
        System.out.println("Boot from root package: com.acme.orders");
    }
}
```

2. OrdersApplication at com.acme.orders — root for scanning.
3. Imports show dependency direction toward domain types.
4. Main at sensible root — frameworks scan downward from here.

### Scene `spring` (renderer: `spring`)

1. Spring Boot scans from main class package down.
2. Too deep main — beans missed mysteriously.
3. Packages are navigation paths for frameworks.

### Scene `deeper` (renderer: `deeper`)

1. Default package — no package declaration — quick demos only, not production.
2. Package naming convention — reversed domain — com.company.product.layer.
3. Never use java or javax as your prefix — reserved and confusing.
4. Split packages — same package name in two JARs — illegal in modules, fragile on classpath.
5. JPMS forbids split packages — migration pain point.
6. package-info.java — package level documentation and annotations.
7. ArchUnit and similar tools test package dependency rules in CI.
8. Feature folders versus layers — both valid — align with team ownership.
9. Monorepo multi-module Maven/Gradle — each module maps to deployable or library boundary.

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
2. One — everything in util.
3. Two — cyclic package dependencies.
4. Three — buried main class.
5. Package names that lie about contents.

### Scene `interview` (renderer: `interview`)

1. Interview — why packages matter?
2. Namespace. Access. Ownership. Framework scanning.
3. Runtime identity — fully qualified name plus classloader.
4. Structure enforces architecture when done honestly.

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

1. Packages group types under namespace.
2. Match folders. Control access. Express ownership.
3. Root package is framework anchor in Spring.
4. Honest tree beats clever naming.

### Scene `teaser` (renderer: `teaser`)

1. Boundaries set. Next — type-safe fixed constants.
2. Episode Thirteen — Enums.
3. States instead of magic strings.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **12** — *Packages*.
- **Series catalog:** Episode 12 ↔ handbook lesson 12 — *Packages*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 12 excerpt)

- Concept: Packages group related Java types under a namespace. They organize code, prevent class-name collisions, define package-private visibility boundaries, and map source structure to runtime class identity. com.acme.orders |-- api |-- domain |-- persistenc

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 12).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Access needs a neighborhood. Packages are those neighborhoods._
- **`title`** — starts from: _Episode Twelve._
- **`namespace`** — starts from: _package com.acme.orders.domain;_
- **`boundary`** — starts from: _Packages define package-private visibility._
- **`structure`** — starts from: _Organize by capability when you can._
- **`spring`** — starts from: _Spring Boot tip — scanning starts from the main class package downward._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why do packages matter?_
- **`teaser`** — starts from: _Boundaries are set. Next — fixed sets of constants with behavior._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
