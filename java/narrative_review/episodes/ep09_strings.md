# Episode 09 — Strings

| Field | Value |
|---|---|
| Episode | 09 |
| Title | Strings |
| Catalog handbook column | 9 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Arrays hold many values. Strings hold text — everywhere in Java.
2. APIs, logs, JSON, SQL, HTTP headers, configuration.
3. String is immutable — powerful safety, easy misuse.
4. Small String mistakes become security and performance incidents.

### Scene `title` (renderer: `title`)

1. Episode Nine.
2. Strings — immutability, equality, and careful construction.

### Scene `immutable` (renderer: `immutable`)

1. Immutable — characters do not change after creation.
2. s = s + world creates new String — old s unchanged.
3. Enables sharing, caching, safe concurrency for read-only text.
4. Careless concatenation in loops allocates repeatedly.
5. Understand create versus mutate — String only creates.

### Scene `equality` (renderer: `equality`)

1. Equality trap again — equals-equals versus equals.
2. Equals-equals — reference identity for objects.
3. Equals — character content comparison.
4. PAID.equals(status) — null-safe literal-first pattern.
5. Make equals your default reflex for text comparison.

### Scene `example` (renderer: `example`)

1. Walk building labels and checking status.
```java
public class LabelBuilder {
    public static String buildLabels(String[] items) {
        StringBuilder sb = new StringBuilder();
        for (String item : items) {
            sb.append(item).append(", ");
        }
        if (sb.length() >= 2) {
            sb.setLength(sb.length() - 2);
        }
        return sb.toString();
    }

    public static boolean isPaid(String status) {
        return "PAID".equals(status); // content equality, null-safe
    }
}
```

2. StringBuilder append in loop — mutates builder, not immutable strings.
3. toString once at end — single allocation burst versus many intermediate strings.
4. isPaid uses PAID.equals(status) — content equality, null-safe.
5. Hot paths need builders. Simple plus is fine for two or three pieces.

### Scene `build` (renderer: `build`)

1. Never plus in tight loops for many pieces.
2. StringBuilder — append, then toString.
3. String.join and String.format for structured assembly.
4. Compilers optimize some simple cases — do not rely on that in hot loops.

### Scene `charset` (renderer: `charset`)

1. Bytes are not characters without charset.
2. StandardCharsets.UTF_8 explicitly when encoding.
3. toLowerCase without Locale can break Turkish I.
4. Never assume platform default charset matches production Linux containers.

### Scene `deeper` (renderer: `deeper`)

1. String pool — literal strings interned in heap string pool.
2. new String("hello") creates separate object — usually avoid unnecessary new.
3. text blocks — triple quotes — multi-line JSON and SQL templates cleanly since Java 15.
4. formatted and formatted methods — String templates evolving — know your JDK version.
5. Regular expressions — String.matches, Pattern.compile — powerful, easy to DoS with catastrophic backtracking.
6. Validate regex complexity on user-supplied patterns.
7. StringTokenizer legacy — prefer split with limit or Scanner for structured parsing.
8. Security — never construct SQL with plus on user input — parameterized queries always.
9. Logging user-controlled strings can be log injection — sanitize or escape.

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
2. One — equals-equals for text.
3. Two — logging secrets in strings.
4. Three — unbounded input strings until OOM.
5. Prefer typed IDs over raw strings twelve layers deep.

### Scene `interview` (renderer: `interview`)

1. Interview — why String immutable?
2. Safety, sharing, stable hash codes for hash maps, simpler concurrency.
3. Use StringBuilder for repeated mutation.
4. Never compare text with equals-equals.

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

### Scene `api` (renderer: `api`)

1. String is UTF-16 — supplementary characters need two char units — surrogate pairs.
2. codePointCount versus length — emoji length surprises in UI validation.
3. StringBuilder initial capacity — new StringBuilder(256) — avoid resize in known size loops.
4. StringJoiner — delimiter prefix suffix — structured concatenation.

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

1. Strings — immutable UTF-16 text objects.
2. equals for content. StringBuilder for loops.
3. Explicit charset. Careful logging.
4. Text is a production type — treat it seriously.

### Scene `teaser` (renderer: `teaser`)

1. Text under control. Next — model the world.
2. Episode Ten — Object-Oriented Programming.
3. Classes, objects, encapsulation.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **9** — *Strings*.
- **Series catalog:** Episode 09 ↔ handbook lesson 9 — *Strings*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 9 excerpt)

- Concept: String represents immutable text in Java. Strings are central to APIs, logging, configuration, SQL, JSON, HTTP, identifiers, and user-visible data. Their immutability supports safety and sharing, but careless use can create memory, encoding, security,
- Mistakes: Common mistakes include using == for comparison, ignoring charset, logging secrets, using regex for simple checks, accepting unbounded string input, lowercasing with default locale, and passing raw strings deep into domain code.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 9).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Arrays hold many values. Strings hold text — and text is everywhere._
- **`title`** — starts from: _Episode Nine._
- **`immutable`** — starts from: _Immutability means the characters never change after creation._
- **`equality`** — starts from: _Equality is the classic trap._
- **`build`** — starts from: _Building strings in a loop?_
- **`charset`** — starts from: _Bytes are not characters without a charset._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why is String immutable?_
- **`teaser`** — starts from: _Text is under control. Next we model the world._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
