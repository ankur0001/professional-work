# Episode 17 — Reflection

| Field | Value |
|---|---|
| Episode | 17 |
| Title | Reflection |
| Catalog handbook column | 17 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Annotations are metadata. Reflection reads type structure at runtime.
2. Discover methods. Invoke by name. Frameworks live here.
3. Powerful — expensive — easy to misuse.

### Scene `title` (renderer: `title`)

1. Episode Seventeen.
2. Reflection — inspect and invoke at runtime.

### Scene `basics` (renderer: `basics`)

1. Class<?> clazz = String.class or obj.getClass().
2. getMethod, getField, getConstructor — discovery API.

### Scene `invoke` (renderer: `invoke`)

1. Method.invoke target with args.
2. setAccessible breaks encapsulation — use rarely.

### Scene `example` (renderer: `example`)

1. Walk invoking String.length reflectively.
```java
import java.lang.reflect.Method;

public class ReflectionDemo {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Class.forName("java.lang.String");
        Method lengthMethod = clazz.getMethod("length");
        Object result = lengthMethod.invoke("hello");
        System.out.println("length = " + result);
    }
}
```

2. Class.forName loads by name.
3. getMethod and invoke — dynamic call slower than direct.

### Scene `frameworks` (renderer: `frameworks`)

1. Spring DI, JSON mappers, ORMs — reflection-heavy.
2. Productivity trade for complexity and startup cost.

### Scene `cost` (renderer: `cost`)

1. Slower than direct calls. Module restrictions. Native image config.
2. Cache MethodHandles in hot paths if unavoidable.

### Scene `safety` (renderer: `safety`)

1. Validate inputs — reflective surfaces can be injection points.
2. Quarantine reflection behind small modules.

### Scene `deeper` (renderer: `deeper`)

1. getDeclaredMethods versus getMethods — declared includes private, getMethods includes inherited public.
2. Constructor.newInstance — replaces deprecated Class.newInstance.
3. Field.get and set — break encapsulation — test utilities sometimes need it.
4. Proxy.newProxyInstance — dynamic interfaces — JDK proxies limited to interfaces.
5. MethodHandles — Java 7+ — faster reflective invoke when cached.
6. VarHandles — atomic access — low-level concurrent field updates.
7. Stack walking — StackWalker API — who called me without full stack trace cost.
8. SecurityManager deprecated — modules and strong encapsulation replace some use cases.

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

1. Reflection instead of interfaces.
2. setAccessible everywhere.
3. Field names as stable API.

### Scene `interview` (renderer: `interview`)

1. Reflection — runtime inspection and invocation.
2. Framework use. Trade flexibility for speed and clarity.

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

### Scene `closing` (renderer: `closing`)

1. Last beat — you now have vocabulary to read JDK release notes and understand what changed.
2. Mark this episode complete in your checklist and skim the handbook revision sheet once.

### Scene `summary` (renderer: `summary`)

1. Reflection enables frameworks.
2. Prefer normal calls when types known.
3. Understand cost and encapsulation risks.

### Scene `teaser` (renderer: `teaser`)

1. Inspect types. Next — cleaner data carriers.
2. Episode Eighteen — Records.
3. Less boilerplate, immutable data.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **17** — *Reflection*.
- **Series catalog:** Episode 17 ↔ handbook lesson 17 — *Reflection*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Annotations are metadata. Reflection is how code reads the structure of types at runtime._
- **`title`** — starts from: _Episode Seventeen._
- **`basics`** — starts from: _Start with Class._
- **`invoke`** — starts from: _Reflection can call methods too._
- **`frameworks`** — starts from: _Why frameworks love reflection._
- **`cost`** — starts from: _Reflection is not free._
- **`safety`** — starts from: _Safety rules of thumb._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is reflection in Java?_
- **`teaser`** — starts from: _We can inspect types. Next — a cleaner way to carry data._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
