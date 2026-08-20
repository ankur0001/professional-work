# Episode 04 — Variables and Data Types

| Field | Value |
|---|---|
| Episode | 04 |
| Title | Variables and Data Types |
| Catalog handbook column | 4 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Three mapped packages and classes.
2. Now — what actually lives inside those fields, parameters, and locals?
3. Variables name values. Types decide what is valid and how operations behave.
4. Pick the wrong type and production pays — overflow, null crashes, rounding bugs on money.
5. Java's type system is strict on purpose. Today we learn to use it as a design tool.

### Scene `title` (renderer: `title`)

1. Episode Four.
2. Variables and Data Types — primitives, references, and real production choices.

### Scene `families` (renderer: `families`)

1. Two families — keep this picture in your head forever.
2. Primitives — raw values stored inline. Eight of them. Never null.
3. References — variables that point to objects on the heap. Can be null.
4. Assignment copies primitive values. Assignment copies reference values — not the whole object.
5. That difference drives memory layout, equality, collections, and API contracts.
6. Confusing the families causes half the NullPointerExceptions in brownfield code.

### Scene `primitives` (renderer: `primitives`)

1. Eight primitives — learn the common four first.
2. int for everyday integers. long for IDs, timestamps, money in minor units.
3. boolean for flags. double for scientific floats — not for currency.
4. byte, short, char, float exist for specialized cases — binary protocols, graphics, legacy APIs.
5. Primitives are fast and compact — no object header, no indirection.
6. They cannot hold null — which eliminates a whole failure class for counters and flags.

### Scene `memory` (renderer: `memory`)

1. Picture memory while you declare variables.
2. int count = 10 — the ten lives in the stack frame as a value.
3. Order order = new Order(...) — order holds a reference; the Order object lives on the heap.
4. final prevents reassigning the variable — not mutating the object it points at.
5. final Order o = ... then o.setStatus(...) may still be legal if the type allows mutation.
6. Deep immutability requires immutable types — records help, coming in Episode Eighteen.

### Scene `example` (renderer: `example`)

1. Walk types you'd see in a payment service.
```java
long amountInCents = 12_345L;
boolean active = true;
String customerId = "C-1001";
var retryCount = 3; // still int at compile time

public record Money(String currency, long minorUnits) {
    public Money {
        if (currency == null || currency.length() != 3) {
            throw new IllegalArgumentException("currency must be ISO-4217");
        }
    }
}
```

2. long amountInCents — store money as integer minor units when rounding rules are simple.
3. boolean active — compact flag, no null unless you choose Boolean wrapper.
4. String customerId — reference type, immutable text, lives on heap.
5. var retryCount = 3 — local type inference. Still statically typed as int — not dynamic typing.
6. record Money — domain type with validation in compact constructor. Currency must be three letters.
7. Types are contracts — especially across APIs, databases, and event payloads.

### Scene `money` (renderer: `money`)

1. Production gotcha — money.
2. Never store currency in double for ledger logic.
3. Binary floating point cannot represent many decimal fractions exactly — 0.1 plus 0.2 drama.
4. Prefer long minor units — cents, paise — or a Money value object.
5. Use BigDecimal when you need explicit decimal scale and rounding modes.
6. Architects standardize this early — fixing money types across services is expensive surgery.
7. Interviewers ask this because teams still ship rounding bugs.

### Scene `wrappers` (renderer: `wrappers`)

1. Wrappers — Integer, Long, Boolean — box primitives into objects.
2. Nullable. Heap allocated. Autoboxing hides conversions.
3. List<Integer> needs objects — autobox on add, unbox on read.
4. A hot loop boxing every int allocates constantly — GC pressure.
5. Prefer primitives in numeric hot paths. Use wrappers when null carries meaning.
6. Episode Fourteen goes deeper on autoboxing traps — today know the cost exists.

### Scene `deeper` (renderer: `deeper`)

1. Go deeper on var — local variable type inference since Java 10.
2. var list = new ArrayList<String>() — compiler infers ArrayList on the right.
3. var is not var in JavaScript — still statically typed.
4. Do not use var when the type is unclear from the right-hand side.
5. var customer = getCustomer() hiding a complex return type hurts readers.
6. Inference is for locals only — not fields, not parameters, not return types.
7. Eight primitives quick reference: byte, short, int, long, float, double, char, boolean.
8. Each has a wrapper except void. char is sixteen-bit UTF-16 code unit — not a full Unicode code point alone.
9. Reference types include classes, interfaces, arrays, enums, records.
10. String is a reference type — immutable object, not a primitive.
11. Choosing long for timestamps in epoch millis avoids Year 2038 int worries on older systems.
12. Instant from java.time — Episode Thirty-One — is the modern timestamp type for new code.

### Scene `mistakes` (renderer: `mistakes`)

1. Three mistakes burned into memory.
2. One — double for money.
3. Two — ignoring integer overflow on counters and limits — silent wrap on int.
4. Three — assuming final means deep immutability.
5. Bonus — overusing String for every domain concept — CustomerId as a type beats naked strings.

### Scene `interview` (renderer: `interview`)

1. Interview question — primitive versus wrapper?
2. Primitive — value, non-null, compact, fast arithmetic.
3. Wrapper — object, nullable, overhead, autoboxing and unboxing risk.
4. Why avoid double for money — binary precision and rounding.
5. What does final mean — no reassignment, not deep immutability.
6. Calm, specific answers beat memorized lists.

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

### Scene `literals` (renderer: `literals`)

1. Literals — 42 int, 42L long, 3.14 double, 3.14f float, 'A' char, true boolean.
2. String literal — double quotes — pooled unless new String forces new object.
3. Underscores in numeric literals — 1_000_000 — readability for cents and millis.
4. Hex and binary — 0xFF, 0b1010 — flags and low-level protocols.
5. Casting — (int) 3.9 truncates toward zero — not rounding — know the difference.
6. Widening conversions automatic — int to long safe. Narrowing needs explicit cast — data loss possible.

### Scene `summary` (renderer: `summary`)

1. Land the plane.
2. Two type families — primitives and references.
3. Choose types for correctness, memory, and API stability.
4. Money belongs in long minor units, BigDecimal, or value objects — not double.
5. final guards variables, not necessarily object contents.
6. Types are contracts — treat them that way across service boundaries.

### Scene `teaser` (renderer: `teaser`)

1. Values have types. Next — operators act on them.
2. Episode Five — Operators.
3. Equality, short-circuit logic, overflow — small symbols, large consequences.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **4** — *Variables and Data Types*.
- **Series catalog:** Episode 04 ↔ handbook lesson 4 — *Variables and Data Types*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 4 excerpt)

- Variables name values, and data types define what values are valid and how operations behave. Java has primitive types for raw values and reference types for objects. For architects, type choices influence correctness, memory footprint, serialization, database
- Java started with eight primitive types and object references. Later releases added autoboxing, generics, var
- Incorrect type choices cause overflow, precision loss, null pointer failures, memory bloat, serialization bugs, and unclear domain models. A money field stored as double
- Java provides primitives for efficient numeric and boolean operations, references for object modeling, String
- Primitive variables hold actual values. Reference variables hold references to heap objects. Assignment copies primitive values or reference values, not full objects. final
- prevents reassignment but does not make referenced objects immutable.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 4).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _In Episode Three, we mapped packages and classes._
- **`title`** — starts from: _Episode Four._
- **`families`** — starts from: _Java has two families of types. Keep this picture._
- **`primitives`** — starts from: _Eight primitives — memorize the common ones first._
- **`memory`** — starts from: _Picture memory._
- **`money`** — starts from: _Production gotcha — money._
- **`wrappers`** — starts from: _Wrappers look similar — Integer, Long, Boolean._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — primitive versus wrapper?_
- **`teaser`** — starts from: _You now know how Java stores meaning._

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
